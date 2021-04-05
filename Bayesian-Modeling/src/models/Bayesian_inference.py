import numpy as np
import pandas as pd
pd.set_option('display.max_rows', 100)
import scipy.sparse as sparse
import pymc3 as pm

from tqdm import tqdm

def determine_c_array(data):
    c = []
    for index, row in  data.iterrows():
        if(row['growth_label_estimate'] == 'minimal'):
            c_value = [1,0,0]
        elif (row['growth_label_estimate'] == 'nochange'):
            c_value = [0,1,0]
        else:
            c_value = [0,0,1]

        c.append(c_value)

    c = np.array(c)
    return c

def run_bayesian_inference(c,labels):
    print(c)
    alphas = np.array([1, 1, 1])

    with pm.Model() as model:
        # Parameters are a dirichlet distribution
        parameters = pm.Dirichlet('parameters', a=alphas, shape=3)
        # Observed data is a multinomial distribution
        observed_data = pm.Multinomial(
            'observed_data', n=1, p=parameters, shape=3, observed=c)

        trace = pm.sample(draws=1000, chains=2, tune=500, discard_tuned_samples=True)
        trace_df = pd.DataFrame(trace['parameters'], columns = labels)

    return trace_df
