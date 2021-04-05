# Bayesian modeling

**Formula:** `P(B/A) ~ = (Cosine_similarity of base and similar county * Bayesian inference of similary county)`

## How the pipeline works?

Update testing.csv file with the proper columns. The sample csv file is in the repository.

## What are the tasks completed in this pipeline

* SARIMAX Time-series prediction for each county
  - including fine-tuning hyperparameter for best performance
* Labeling data for [ minimal, nochange, widespread]
* Determine Bayesian inference for all the three labels 
* Compute Bayesian probability for all the three labels [ y_pred ]
* Label real world data [ y_actual ]
* Measure Mean square error, Root mean square error metrics

## Prerequisite to run this pipeline

* compute cosine similarity for PCA columns between base region and other regions in the segment


## command to run the pipeline
cd Bayesian-Modeling/src/
`python compute_bayesian_probability.py`


