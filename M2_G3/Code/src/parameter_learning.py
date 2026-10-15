"""Small validation-grid parameter tuning for the TTT-style Gaussian model.

This is M2 hyperparameter selection, not a claim of full marginal-likelihood/evidence
maximization. The grid is selected by forward validation log-loss on synthetic matches.
"""
import argparse,csv,os
import numpy as np
from skill_models import generate_synthetic,win_probability,log_loss,_trueskill_pair_update


def score_candidate(matches,n_players,n_times,process_var,beta=1.0,prior_var=36.0):
    by_time=[[] for _ in range(n_times)]
    for m in matches: by_time[m['time']].append(m)
    mu=np.zeros(n_players); var=np.full(n_players,prior_var); probs=[]; labels=[]
    for t,ms in enumerate(by_time):
        if t>0: var+=process_var
        train=[m for j,m in enumerate(ms) if j%5!=0]
        valid=[m for j,m in enumerate(ms) if j%5==0]
        for m in train:
            a,b=m['a'],m['b']; ma,va,mb,vb=_trueskill_pair_update(mu[a],var[a],mu[b],var[b],m['y_a'],beta)
            mu[a],var[a],mu[b],var[b]=ma,va,mb,vb
        for m in valid:
            probs.append(win_probability(mu[m['a']],var[m['a']],mu[m['b']],var[m['b']],beta)); labels.append(m['y_a'])
    return log_loss(probs,labels),len(labels)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--seed',type=int,default=42);ap.add_argument('--out',default='../../Results/parameter_grid.csv');args=ap.parse_args()
    skills,matches=generate_synthetic(seed=args.seed)
    rows=[]
    for q in (0.05**2,0.15**2,0.22**2,0.35**2,0.50**2):
        for beta in (0.7,1.0,1.3):
            loss,n=score_candidate(matches,skills.shape[1],skills.shape[0],q,beta)
            rows.append({'process_var':q,'beta':beta,'validation_logloss':loss,'validation_matches':n,'seed':args.seed})
    rows.sort(key=lambda x:x['validation_logloss'])
    path=os.path.abspath(os.path.join(os.path.dirname(__file__),args.out));os.makedirs(os.path.dirname(path),exist_ok=True)
    with open(path,'w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    print('Best validation setting:',rows[0]);print('Full grid written:',path)
if __name__=='__main__':main()
