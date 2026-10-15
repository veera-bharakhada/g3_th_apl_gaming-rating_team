"""Reproducible synthetic benchmark for M2; writes raw runs and sensitivity runs."""
import argparse,csv,json,os
import numpy as np
from skill_models import evaluate


def write_csv(path,rows):
    if not rows: return
    with open(path,'w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--runs',type=int,default=10);ap.add_argument('--seed',type=int,default=42)
    ap.add_argument('--out',default='../../Results');ap.add_argument('--sensitivity',action='store_true');args=ap.parse_args()
    out=os.path.abspath(os.path.join(os.path.dirname(__file__),args.out));os.makedirs(out,exist_ok=True)
    rows=[evaluate(seed=args.seed+i) for i in range(args.runs)]
    write_csv(os.path.join(out,'synthetic_runs.csv'),rows)
    sens=[]
    if args.sensitivity:
        for sd in (0.05,0.15,0.30,0.50):
            for i in range(args.runs): sens.append(evaluate(seed=args.seed+i,skill_step_sd=sd))
        write_csv(os.path.join(out,'sensitivity.csv'),sens)
    metrics=[k for k,v in rows[0].items() if isinstance(v,(int,float)) and k not in ('seed','n_matches','n_players','n_times','ttt_ep_iterations','ttt_ep_converged','skill_step_sd','process_var','beta')]
    summary={'runs':args.runs,'seed_start':args.seed,'settings':{'players':8,'time_steps':30,'matches_per_time':10,'skill_step_sd':0.22,'beta':1.0,'process_var':0.22**2},
      'mean':{k:float(np.mean([r[k] for r in rows])) for k in metrics},
      'sample_sd':{k:float(np.std([r[k] for r in rows],ddof=1)) if len(rows)>1 else 0.0 for k in metrics},
      'ttt_ep_convergence_rate':float(np.mean([r['ttt_ep_converged'] for r in rows])),
      'ttt_ep_mean_iterations':float(np.mean([r['ttt_ep_iterations'] for r in rows])),
      'runtime_note':'Wall-clock values are small-workload measurements and hardware-dependent.'}
    with open(os.path.join(out,'summary.json'),'w') as f:json.dump(summary,f,indent=2)
    print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
