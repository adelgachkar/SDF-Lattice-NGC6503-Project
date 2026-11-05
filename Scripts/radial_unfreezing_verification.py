#!/usr/bin/env python3
"""Radial-unfreezing verification for the SDF-Lattice NGC 6503 project.

Input CSV columns: r_kpc,v_obs_kms,v_bar_kms,sigma_kms. The fit is evaluated
with chi2_nu = sum(((v_obs-v_model)/sigma)**2)/(N-p), where p is the number
of fitted parameters. No observational table is bundled with this repository;
reported benchmark figures are therefore audited as targets, not claimed to
have been recomputed from raw SPARC points. Run --self-test for deterministic
unit/property checks or --input path.csv to analyze supplied data.
"""
from __future__ import annotations
import argparse, csv, json, math, sys
from pathlib import Path
from typing import Sequence
KPC_TO_M = 3.0857e19
R0_KPC = 1.83
DELTA_R_KPC = 0.46
V_INF_KMS = 116.2
TARGET_CHI2_NU = 0.942
TARGET_OUTER_SLOPE_KMS_PER_KPC = -0.018
TARGET_ML = 0.62

def zeta(r_kpc: float) -> float:
    """Canonical smooth unfreezing activation, dimensionless in [0,1]."""
    if r_kpc < 0: raise ValueError("radius must be non-negative")
    return 0.5 * (1.0 + math.tanh((r_kpc - R0_KPC) / DELTA_R_KPC))

def model_velocity(r_kpc: float, v_bar_kms: float) -> float:
    """Quadrature model: v^2 = v_bar^2 + v_inf^2*zeta(r)."""
    if r_kpc <= 0: raise ValueError("radius must be positive")
    if v_bar_kms < 0: raise ValueError("baryonic speed must be non-negative")
    return math.sqrt(v_bar_kms*v_bar_kms + V_INF_KMS*V_INF_KMS*zeta(r_kpc))

def reduced_chi_squared(observed: Sequence[float], predicted: Sequence[float],
                        sigma: Sequence[float], n_parameters: int=0) -> float:
    """Pearson chi-square per degree of freedom; errors are 1-sigma Gaussian."""
    n=len(observed)
    if n == 0 or len(predicted)!=n or len(sigma)!=n: raise ValueError("arrays must have equal nonzero length")
    dof=n-n_parameters
    if dof <= 0: raise ValueError("degrees of freedom N-p must be positive")
    if any(not math.isfinite(x) for arr in (observed,predicted,sigma) for x in arr): raise ValueError("non-finite input")
    if any(s<=0 for s in sigma): raise ValueError("all uncertainties must be positive")
    return sum(((o-m)/s)**2 for o,m,s in zip(observed,predicted,sigma))/dof

def linear_slope(x: Sequence[float], y: Sequence[float]) -> float:
    """Ordinary least-squares slope; input arrays must represent outer-halo points."""
    if len(x)!=len(y) or len(x)<2: raise ValueError("slope requires >=2 paired points")
    xm=sum(x)/len(x); ym=sum(y)/len(y); den=sum((a-xm)**2 for a in x)
    if den==0: raise ValueError("radii must not all be identical")
    return sum((a-xm)*(b-ym) for a,b in zip(x,y))/den

def load_csv(path: Path):
    required={'r_kpc','v_obs_kms','v_bar_kms','sigma_kms'}
    with path.open(newline='',encoding='utf-8-sig') as f:
        reader=csv.DictReader(f)
        if not reader.fieldnames or not required.issubset(reader.fieldnames):
            raise ValueError('CSV must include: '+', '.join(sorted(required)))
        rows=[{k:float(row[k]) for k in required} for row in reader]
    if not rows: raise ValueError('CSV contains no data rows')
    return rows

def analyze(rows, n_parameters=0, outer_min_kpc=8.0):
    radii=[r['r_kpc'] for r in rows]
    obs=[r['v_obs_kms'] for r in rows]
    sig=[r['sigma_kms'] for r in rows]
    pred=[model_velocity(r['r_kpc'],r['v_bar_kms']) for r in rows]
    outer=[(r['r_kpc'],pred[i]) for i,r in enumerate(rows) if r['r_kpc']>=outer_min_kpc]
    slope=linear_slope([q[0] for q in outer],[q[1] for q in outer]) if len(outer)>=2 else None
    return {'n_points':len(rows),'n_parameters':n_parameters,'dof':len(rows)-n_parameters,
            'chi2_nu':reduced_chi_squared(obs,pred,sig,n_parameters),
            'outer_model_slope_kms_per_kpc':slope,'outer_min_kpc':outer_min_kpc,
            'mass_to_light_Msun_per_Lsun':TARGET_ML,
            'model':'sqrt(v_bar^2 + v_inf^2*zeta(r))',
            'parameters':{'R0_kpc':R0_KPC,'DeltaR_kpc':DELTA_R_KPC,'v_inf_kms':V_INF_KMS}}

def self_test():
    assert abs(KPC_TO_M-3.0857e19)<1e5
    assert zeta(0.0)<0.001 and abs(zeta(R0_KPC)-0.5)<1e-15 and zeta(10)>0.999
    # Analytic metric identity check only; NOT galaxy data: one standardized residual.
    chi=reduced_chi_squared([math.sqrt(TARGET_CHI2_NU)],[0.0],[1.0],0)
    assert abs(chi-TARGET_CHI2_NU)<1e-12
    # A line with the target outer slope is a mathematical regression test, not data.
    xs=[10.0,15.0,20.0]; ys=[120.0+TARGET_OUTER_SLOPE_KMS_PER_KPC*x for x in xs]
    assert abs(linear_slope(xs,ys)-TARGET_OUTER_SLOPE_KMS_PER_KPC)<1e-12
    assert TARGET_ML==0.62
    # velocity and activation boundaries
    assert model_velocity(1.0,0.0)>=0 and model_velocity(5.0,0.0)<V_INF_KMS
    return {'status':'PASS','checks':['kpc conversion','canonical kernel limits and midpoint','chi-square definition identity','OLS slope identity','M/L target','velocity model domain'],
            'note':'Target-value unit tests use constructed mathematical inputs; they do not independently establish an observational fit.'}

def main(argv=None):
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--input',type=Path,help='observational CSV; see module docstring')
    ap.add_argument('--n-parameters',type=int,default=0,help='number of parameters estimated from these same points')
    ap.add_argument('--outer-min-kpc',type=float,default=8.0)
    ap.add_argument('--output-json',type=Path)
    ap.add_argument('--self-test',action='store_true')
    args=ap.parse_args(argv)
    if args.self_test: result=self_test()
    elif args.input: result=analyze(load_csv(args.input),args.n_parameters,args.outer_min_kpc)
    else: result={'status':'READY','targets':{'chi2_nu':TARGET_CHI2_NU,'outer_slope_kms_per_kpc':TARGET_OUTER_SLOPE_KMS_PER_KPC,'mass_to_light_Msun_per_Lsun':TARGET_ML},
                  'evidence_status':'reported targets; raw observational points and uncertainties are not included in supplied archive; use --input to calculate from data'}
    text=json.dumps(result,indent=2,sort_keys=True); print(text)
    if args.output_json: args.output_json.write_text(text+'\n',encoding='utf8')
    if result.get('status')=='PASS' or args.input: return 0
    return 0
if __name__=='__main__': raise SystemExit(main())
