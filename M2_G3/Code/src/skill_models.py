"""Small binary-outcome TrueSkill/TTT-style Gaussian message-passing prototype.

The implementation follows the two-player, no-draw equations in Landfried & Mocskos
(2025): Gaussian skill priors, Gaussian performance noise beta, probit win likelihood,
truncated-normal moment matching, and forward/backward temporal information flow.
It is an educational, single-player-per-side implementation; it does NOT implement
all multi-team/draw handling or every optimization in the published package.
"""
from __future__ import annotations
import math, time
import numpy as np
from scipy.special import ndtr
from scipy.stats import norm


def log_loss(probs, labels):
    p=np.clip(np.asarray(probs,dtype=float),1e-12,1-1e-12); y=np.asarray(labels,dtype=float)
    return float(-np.mean(y*np.log(p)+(1-y)*np.log(1-p)))


def brier_score(probs, labels):
    return float(np.mean((np.asarray(probs,dtype=float)-np.asarray(labels,dtype=float))**2))


def win_probability(mu_a, var_a, mu_b, var_b, beta=1.0):
    """P(A wins) under paper's Gaussian performance/probit model (Eq. 1)."""
    c=math.sqrt(max(var_a+var_b+2.0*beta*beta,1e-12))
    return float(ndtr((mu_a-mu_b)/c))


def generate_synthetic(seed=42,n_players=8,n_times=30,matches_per_time=10,
                       skill_step_sd=0.22,beta=1.0):
    """Generate known random-walk skills and match results under Gaussian performance."""
    rng=np.random.default_rng(seed)
    skills=np.zeros((n_times,n_players),dtype=float)
    skills[0]=rng.normal(0,0.8,n_players)
    for t in range(1,n_times):
        skills[t]=skills[t-1]+rng.normal(0,skill_step_sd,n_players)
    matches=[]
    for t in range(n_times):
        seen=set(); attempts=0
        while len(seen)<matches_per_time and attempts<matches_per_time*50:
            attempts+=1; a,b=map(int,rng.choice(n_players,size=2,replace=False))
            pair=tuple(sorted((a,b)))
            if pair in seen: continue
            seen.add(pair)
            pa=float(ndtr((skills[t,a]-skills[t,b])/math.sqrt(2*beta*beta)))
            winner=a if rng.random()<pa else b
            matches.append({'time':t,'a':a,'b':b,'winner':int(winner),'loser':int(b if winner==a else a),
                            'y_a':int(winner==a),'p_true_a':pa})
    return skills,matches


def constant_predict(matches):
    y=np.asarray([m['y_a'] for m in matches],dtype=float)
    return np.full(len(matches),0.5),y


def elo_predict(matches,n_players,k=24.0,base=400.0):
    ratings=np.full(n_players,1500.0); probs=[]; labels=[]
    for m in sorted(matches,key=lambda x:(x['time'],x.get('order',0))):
        a,b=m['a'],m['b']; p=1/(1+10**((ratings[b]-ratings[a])/base))
        probs.append(p); labels.append(m['y_a']); actual=float(m['y_a'])
        ratings[a]+=k*(actual-p); ratings[b]-=k*(actual-p)
    return np.asarray(probs),np.asarray(labels),ratings


def _trueskill_pair_update(mu_a,var_a,mu_b,var_b,y_a,beta=1.0):
    """Moment-match posterior skill marginals for one observed binary outcome.

    Implements the standard two-player no-draw TrueSkill update derived from the
    truncated Gaussian performance difference in Landfried & Mocskos (2025), Sec. 3.4–3.6.
    Returns posterior means and variances for each player's cavity distributions.
    """
    c2=max(var_a+var_b+2*beta*beta,1e-12); c=math.sqrt(c2)
    # Orient the difference so that the observed winner is the positive side.
    sign=1.0 if y_a==1 else -1.0
    t=sign*(mu_a-mu_b)/c
    # Mills ratio for a one-sided truncated standard normal. Clip for numerical stability.
    denom=max(float(ndtr(t)),1e-14)
    v=float(norm.pdf(t)/denom)
    w=v*(v+t)
    # Standard TrueSkill Gaussian moment update; w is nonnegative in normal regimes.
    va=max(var_a*(1.0-(var_a/c2)*w),1e-9)
    vb=max(var_b*(1.0-(var_b/c2)*w),1e-9)
    ma=mu_a+sign*(var_a/c)*v
    mb=mu_b-sign*(var_b/c)*v
    return ma,va,mb,vb


def _gaussian_to_natural(mu,var):
    var=max(float(var),1e-9); tau=1.0/var; eta=float(mu)*tau
    return tau,eta


def _natural_to_gaussian(tau,eta):
    tau=max(float(tau),1e-9); return float(eta/tau),float(1.0/tau)


def _build_temporal_prior(n_players,n_times,prior_var,process_var):
    """Precision and information vector for Gaussian random walks.

    process_var may be a scalar (homogeneous drift) or a [time, player] array
    specifying the transition variance from t-1 to t for each player.
    """
    d=n_players*n_times; precision=np.zeros((d,d)); eta=np.zeros(d)
    for p in range(n_players): precision[p,p]+=1.0/prior_var
    q=np.asarray(process_var,dtype=float)
    if q.ndim==0:
        q=np.full((n_times,n_players),float(q))
    elif q.shape!=(n_times,n_players):
        raise ValueError(f"process_var array must have shape {(n_times,n_players)}, got {q.shape}")
    for t in range(1,n_times):
        for p in range(n_players):
            qinv=1.0/max(float(q[t,p]),1e-9)
            i=(t-1)*n_players+p; j=t*n_players+p
            precision[i,i]+=qinv; precision[j,j]+=qinv
            precision[i,j]-=qinv; precision[j,i]-=qinv
    return precision,eta


def ttt_ep_smoother(matches,n_players,n_times,prior_var=36.0,process_var=0.22**2,
                    beta=1.0,max_iter=100,tol=1e-3,damping=0.5):
    """Iterative Gaussian message-passing smoother for binary two-player matches.

    Each match factor sends Gaussian likelihood messages to its two skill-time variables.
    Messages are updated by moment matching the paper's truncated-normal outcome posterior.
    Temporal Gaussian random-walk factors allow evidence to flow forward and backward.
    This is a small-scale EP/loopy-message-passing implementation for M2, not the full
    published package (no draws, multi-team outcomes, or sparse large-scale solver).
    Returns means, marginal variances, iteration count, convergence flag.
    """
    d=n_players*n_times; baseP,baseEta=_build_temporal_prior(n_players,n_times,prior_var,process_var)
    # One Gaussian likelihood message per match endpoint, represented in natural parameters.
    mtau=np.zeros((len(matches),2)); meta=np.zeros((len(matches),2))
    means=np.zeros(d); variances=np.ones(d)*prior_var
    converged=False
    for it in range(1,max_iter+1):
        P=baseP.copy(); eta=baseEta.copy()
        for k,m in enumerate(matches):
            for side,p in enumerate((m['a'],m['b'])):
                idx=m['time']*n_players+p
                P[idx,idx]+=mtau[k,side]; eta[idx]+=meta[k,side]
        P+=np.eye(d)*1e-8
        try:
            means=np.linalg.solve(P,eta)
            cov=np.linalg.inv(P)
        except np.linalg.LinAlgError:
            cov=np.linalg.pinv(P); means=cov@eta
        variances=np.maximum(np.diag(cov),1e-8)
        max_change=0.0
        for k,m in enumerate(matches):
            ia=m['time']*n_players+m['a']; ib=m['time']*n_players+m['b']
            # Cavity distributions remove this match's own incoming message.
            ca_tau=max(1.0/variances[ia]-mtau[k,0],1e-8)
            cb_tau=max(1.0/variances[ib]-mtau[k,1],1e-8)
            ca_eta=means[ia]/variances[ia]-meta[k,0]
            cb_eta=means[ib]/variances[ib]-meta[k,1]
            ca_mu,ca_var=_natural_to_gaussian(ca_tau,ca_eta)
            cb_mu,cb_var=_natural_to_gaussian(cb_tau,cb_eta)
            pa_mu,pa_var,pb_mu,pb_var=_trueskill_pair_update(ca_mu,ca_var,cb_mu,cb_var,m['y_a'],beta)
            na_tau,na_eta=_gaussian_to_natural(pa_mu,pa_var)
            nb_tau,nb_eta=_gaussian_to_natural(pb_mu,pb_var)
            new_a_tau=max(na_tau-ca_tau,0.0); new_b_tau=max(nb_tau-cb_tau,0.0)
            new_a_eta=na_eta-ca_eta; new_b_eta=nb_eta-cb_eta
            for side,(nt,ne) in enumerate(((new_a_tau,new_a_eta),(new_b_tau,new_b_eta))):
                oldt,olde=mtau[k,side],meta[k,side]
                mtau[k,side]=(1-damping)*oldt+damping*nt
                meta[k,side]=(1-damping)*olde+damping*ne
                max_change=max(max_change,abs(mtau[k,side]-oldt),abs(meta[k,side]-olde))
        if max_change<tol:
            converged=True; break
    # Recompute final marginals after last message update.
    P=baseP.copy(); eta=baseEta.copy()
    for k,m in enumerate(matches):
        for side,p in enumerate((m['a'],m['b'])):
            idx=m['time']*n_players+p; P[idx,idx]+=mtau[k,side]; eta[idx]+=meta[k,side]
    P+=np.eye(d)*1e-8
    means=np.linalg.solve(P,eta); cov=np.linalg.inv(P); variances=np.maximum(np.diag(cov),1e-8)
    return means.reshape(n_times,n_players),variances.reshape(n_times,n_players),it,converged


def forward_trueskill_filter(matches,n_players,n_times,prior_var=36.0,process_var=0.22**2,beta=1.0):
    """Chronological TrueSkill-style filtering; later results never revise earlier states."""
    mu=np.zeros(n_players); var=np.full(n_players,prior_var); means=np.zeros((n_times,n_players)); vars_=np.zeros_like(means)
    by_time=[[] for _ in range(n_times)]
    for m in matches: by_time[m['time']].append(m)
    for t in range(n_times):
        if t>0: var=var+process_var
        for m in by_time[t]:
            a,b=m['a'],m['b']; ma,va,mb,vb=_trueskill_pair_update(mu[a],var[a],mu[b],var[b],m['y_a'],beta)
            mu[a],var[a],mu[b],var[b]=ma,va,mb,vb
        means[t]=mu; vars_[t]=var
    return means,vars_


def evaluate(seed=42,n_players=8,n_times=30,matches_per_time=10,skill_step_sd=0.22,
             process_var=0.22**2,beta=1.0):
    skills,matches=generate_synthetic(seed,n_players,n_times,matches_per_time,skill_step_sd,beta)
    const_p,labels=constant_predict(matches)
    t0=time.perf_counter(); elo_p,elo_y,_=elo_predict(matches,n_players); elo_sec=time.perf_counter()-t0
    t0=time.perf_counter(); fmu,fvar=forward_trueskill_filter(matches,n_players,n_times,process_var=process_var,beta=beta); fsec=time.perf_counter()-t0
    t0=time.perf_counter(); smu,svar,n_iter,converged=ttt_ep_smoother(matches,n_players,n_times,process_var=process_var,beta=beta); ssec=time.perf_counter()-t0
    # Relative skill is identifiable; center each time slice before comparing with truth.
    truth=skills-skills.mean(axis=1,keepdims=True); fc=fmu-fmu.mean(axis=1,keepdims=True); sc=smu-smu.mean(axis=1,keepdims=True)
    # Forward-only prediction probabilities are recorded before assimilating each result.
    # A separate chronological scoring pass avoids using post-match ratings to predict that match.
    pred=[]; y=[]; rating_mu=np.zeros(n_players); rating_var=np.full(n_players,36.0); by_time=[[] for _ in range(n_times)]
    for m in matches: by_time[m['time']].append(m)
    for t in range(n_times):
        if t>0: rating_var+=process_var
        for m in by_time[t]:
            a,b=m['a'],m['b']; pred.append(win_probability(rating_mu[a],rating_var[a],rating_mu[b],rating_var[b],beta)); y.append(m['y_a'])
            ma,va,mb,vb=_trueskill_pair_update(rating_mu[a],rating_var[a],rating_mu[b],rating_var[b],m['y_a'],beta)
            rating_mu[a],rating_var[a],rating_mu[b],rating_var[b]=ma,va,mb,vb
    return {'seed':seed,'n_matches':len(matches),'n_players':n_players,'n_times':n_times,
      'constant_logloss':log_loss(const_p,labels),'constant_brier':brier_score(const_p,labels),
      'elo_logloss':log_loss(elo_p,elo_y),'elo_brier':brier_score(elo_p,elo_y),'elo_runtime_sec':elo_sec,
      'forward_skill_mae':float(np.mean(np.abs(fc-truth))),'forward_runtime_sec':fsec,
      'ttt_ep_skill_mae':float(np.mean(np.abs(sc-truth))),'ttt_ep_runtime_sec':ssec,
      'ttt_ep_iterations':n_iter,'ttt_ep_converged':int(converged),
      'forward_logloss':log_loss(pred,y),'forward_brier':brier_score(pred,y),
      'skill_step_sd':skill_step_sd,'process_var':process_var,'beta':beta}
