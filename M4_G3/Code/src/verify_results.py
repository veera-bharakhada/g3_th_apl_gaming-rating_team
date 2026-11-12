from pathlib import Path
import csv,json,statistics
root=Path(__file__).resolve().parents[1]
rows=list(csv.DictReader((root/'Results/main_10_seed_results.csv').open()))
assert len(rows)==20
assert sorted({int(r['seed']) for r in rows})==list(range(42,52))
for metric in ('MAE','RMSE','logloss','brier'):
    for model in ('baseline','extension'):
        vals=[float(r[metric]) for r in rows if r['model']==model]
        print(f'{metric:9} {model:9} {statistics.mean(vals):.4f} +/- {statistics.stdev(vals):.4f}')
paired=json.loads((root/'Results/paired_mae_test.json').read_text())
print('Paired MAE reduction:',paired['mean_baseline_minus_extension_mae'])
print('p-value:',paired['p_value'])
print('Bootstrap CI:',paired['bootstrap_95_ci'])
assert paired['p_value']<0.05
print('Archived results verification passed')
