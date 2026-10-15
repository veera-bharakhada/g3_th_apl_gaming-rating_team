import os,json
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import ttest_rel
ROOT=os.path.dirname(__file__); df=pd.read_csv(os.path.join(ROOT,'synthetic_runs.csv'))
sens_path=os.path.join(ROOT,'sensitivity.csv')
if os.path.exists(sens_path): sens=pd.read_csv(sens_path)
# Skill-recovery comparison
cols=['forward_skill_mae','ttt_ep_skill_mae']; labels=['Forward-only TrueSkill-style','TTT-style EP smoother']
plt.figure(figsize=(7.2,4.6)); means=[df[c].mean() for c in cols]; errs=[df[c].std(ddof=1) for c in cols]
plt.bar(labels,means,yerr=errs,capsize=5);plt.ylabel('Centered skill MAE (lower is better)');plt.title(f'Synthetic skill recovery ({len(df)} seeds)');plt.xticks(rotation=8);plt.tight_layout();plt.savefig(os.path.join(ROOT,'skill_mae_comparison.png'),dpi=180);plt.close()
# Forecasting baselines
pred_cols=['constant_logloss','elo_logloss','forward_logloss']; pred_labels=['Constant','Elo','Forward-only']
plt.figure(figsize=(7.2,4.6));plt.bar(pred_labels,[df[c].mean() for c in pred_cols],yerr=[df[c].std(ddof=1) for c in pred_cols],capsize=5)
plt.ylabel('Chronological pre-match log-loss (lower is better)');plt.title(f'Prediction baseline comparison ({len(df)} seeds)');plt.tight_layout();plt.savefig(os.path.join(ROOT,'prediction_logloss.png'),dpi=180);plt.close()
# Sensitivity
if os.path.exists(sens_path):
 agg=sens.groupby('skill_step_sd').agg(fwd=('forward_skill_mae','mean'),ttt=('ttt_ep_skill_mae','mean'),fwd_sd=('forward_skill_mae','std'),ttt_sd=('ttt_ep_skill_mae','std')).reset_index()
 plt.figure(figsize=(7.2,4.6));plt.errorbar(agg.skill_step_sd,agg.fwd,yerr=agg.fwd_sd,marker='o',capsize=4,label='Forward-only')
 plt.errorbar(agg.skill_step_sd,agg.ttt,yerr=agg.ttt_sd,marker='o',capsize=4,label='TTT-style EP smoother')
 plt.xlabel('True skill-change SD per time step');plt.ylabel('Centered skill MAE');plt.title('Sensitivity to skill dynamics');plt.legend();plt.tight_layout();plt.savefig(os.path.join(ROOT,'sensitivity_plot.png'),dpi=180);plt.close()
 paired=ttest_rel(df.forward_skill_mae,df.ttt_ep_skill_mae)
 summary={'runs':len(df),'seeds':df.seed.astype(int).tolist(),'settings':{'players':8,'time_steps':30,'matches_per_time':10,'skill_step_sd':0.22,'beta':1.0,'process_var':0.22**2,'model':'restricted binary two-player TTT-style EP prototype'},'means':{c:float(df[c].mean()) for c in ['constant_logloss','constant_brier','elo_logloss','elo_brier','forward_logloss','forward_brier','forward_skill_mae','ttt_ep_skill_mae','elo_runtime_sec','forward_runtime_sec','ttt_ep_runtime_sec','ttt_ep_iterations','ttt_ep_converged']},
 'sample_sd':{c:float(df[c].std(ddof=1)) for c in ['constant_logloss','constant_brier','elo_logloss','elo_brier','forward_logloss','forward_brier','forward_skill_mae','ttt_ep_skill_mae','elo_runtime_sec','forward_runtime_sec','ttt_ep_runtime_sec']},
 'paired_skill_mae_test':{'mean_forward_minus_ttt_ep':float((df.forward_skill_mae-df.ttt_ep_skill_mae).mean()),'t_statistic':float(paired.statistic),'p_value':float(paired.pvalue)},
 'ttt_ep_convergence_rate':float(df.ttt_ep_converged.mean()),'note':'Synthetic results only; this is a TTT-style binary EP prototype, not full package reproduction. Runtime is hardware-dependent.'}
 with open(os.path.join(ROOT,'summary.json'),'w') as f:json.dump(summary,f,indent=2)
 print(json.dumps(summary,indent=2))
