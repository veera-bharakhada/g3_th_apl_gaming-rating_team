# Data

## Primary Dataset: ATP Tennis Match History
- Source: https://github.com/glandfried/tennis_atp/releases/download/atp/history.csv.zip
- Original data: https://github.com/JeffSackmann/tennis_atp
- ~447,000 singles and doubles matches (1915–2020), 19,000+ players
- Fields: players, singles/doubles, tournament name & date, round, surface

## Replication Reference
Official replication package (base paper): 
https://www.jstatsoft.org/index.php/jss/article/view/v112i06

## Synthetic Dataset
A small synthetic dataset with a known ground-truth skill trajectory will be generated 
to validate model correctness before running on real data. Generation script: `generate_synthetic.py` (to be added).

## Usage Notes
- Raw data is not committed directly if size/license requires a download script instead — see `download_data.py` (to be added).
- Processed/cleaned data will be documented here once preprocessing is finalized.
