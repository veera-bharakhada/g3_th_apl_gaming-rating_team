"""M2 original extension pilot: activity-aware temporal skill variance.

This module tests a concrete extension of the homogeneous random-walk prior:
players who participate in a time step use q_active; players who are inactive
use a larger q_idle. The activity state is observed from the synthetic match
schedule, not secretly inferred from outcomes. This is a controlled simulation,
not an ATP result and not a claim that inactivity necessarily lowers mean skill.
"""
from __future__ import annotations
import csv, json, os, sys, time
import numpy as np
from scipy.special import ndtr
HERE=os.path.dirname(__file__)
if HERE not in sys.path: sys.path.insert(0,HERE)
from skill_models import ttt_ep_smoother


def generate_activity_data(seed=2026, n_players=8, n_times=24, matches_per_time=3,
                           q_active=0.02**2, q_idle=0.22**2, beta=1.0):
    rng=np.random.default_rng(seed)
    schedule=[]; active=np.zeros((n_times,n_players),dtype=bool)
    for t in range(n_times):
        pairs=set(); attempts=0
        while len(pairs)<matches_per_time and attempts<10000:
            attempts+=1
            a,b=sorted(map(int,rng.choice(n_players,2,replace=False)))
            pairs.add((a,b))
        for a,b in sorted(pairs):
            schedule.append({'time':t,'a':a,'b':b})
            active[t,a]=True; active[t,b]=True
    truth=np.zeros((n_times,n_players)); truth[0]=rng.normal(0,0.8,n_players)
    q=np.full((n_times,n_players),q_idle,dtype=float)
    q[0,:]=q_active
    for t in range(1,n_times):
        q[t]=np.where(active[t],q_active,q_idle)
        truth[t]=truth[t-1]+rng.normal(0,np.sqrt(q[t]),n_players)
    matches=[]
    for m in schedule:
        a,b,t=m['a'],m['b'],m['time']
        p=float(ndtr((truth[t,a]-truth[t,b])/np.sqrt(2*beta*beta)))
        ya=int(rng.random()<p)
        matches.append({**m,'winner':a if ya else b,'loser':b if ya else a,'y_a':ya,'p_true_a':p})
    return truth,matches,active,q


def center(x): return x-x.mean(axis=1,keepdims=True)

def run(seed=2026):
    truth,matches,active,q=generate_activity_data(seed=seed)
    n_times,n_players=truth.shape
    t0=time.perf_counter()
    fixed_mu,fixed_var,fixed_it,fixed_conv=ttt_ep_smoother(
        matches,n_players,n_times,process_var=0.08**2,max_iter=100,tol=1e-3)
    fixed_sec=time.perf_counter()-t0
    t0=time.perf_counter()
    aware_mu,aware_var,aware_it,aware_conv=ttt_ep_smoother(
        matches,n_players,n_times,process_var=q,max_iter=100,tol=1e-3)
    aware_sec=time.perf_counter()-t0
    truth_c=center(truth); fixed_c=center(fixed_mu); aware_c=center(aware_mu)
    mae_fixed=float(np.mean(np.abs(truth_c-fixed_c)))
    mae_aware=float(np.mean(np.abs(truth_c-aware_c)))
    return {
      'seed':seed,'matches':len(matches),'players':n_players,'time_steps':n_times,
      'active_transition_variance':0.02**2,'inactive_transition_variance':0.22**2,
      'fixed_variance_assumption':0.08**2,
      'fixed_drift_skill_mae':mae_fixed,'activity_aware_skill_mae':mae_aware,
      'fixed_drift_runtime_sec':fixed_sec,'activity_aware_runtime_sec':aware_sec,
      'fixed_drift_iterations':fixed_it,'activity_aware_iterations':aware_it,
      'fixed_drift_converged':int(fixed_conv),'activity_aware_converged':int(aware_conv),
      'inactive_player_time_fraction':float(1-active.mean())
    }

def main():
    out=os.path.abspath(os.path.join(HERE,'../../Results')); os.makedirs(out,exist_ok=True)
    rows=[run(2026+i) for i in range(5)]
    with open(os.path.join(out,'activity_aware_extension.csv'),'w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    keys=['fixed_drift_skill_mae','activity_aware_skill_mae','fixed_drift_runtime_sec','activity_aware_runtime_sec','fixed_drift_iterations','activity_aware_iterations','inactive_player_time_fraction']
    summary={'runs':len(rows),'seeds':[r['seed'] for r in rows], 'means':{k:float(np.mean([r[k] for r in rows])) for k in keys},
             'standard_deviations':{k:float(np.std([r[k] for r in rows],ddof=1)) for k in keys},
             'interpretation':'Pilot synthetic test of activity-dependent transition variance. Do not generalize to real ATP data; activity is observed from the generated schedule and the two variance levels are known by construction.'}
    with open(os.path.join(out,'activity_aware_summary.json'),'w') as f: json.dump(summary,f,indent=2)
    print(json.dumps(summary,indent=2))
if __name__=='__main__': main()
