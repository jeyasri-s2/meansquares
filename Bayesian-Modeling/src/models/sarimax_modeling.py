import pandas as pd
import numpy as np
from statsmodels.tsa.statespace.sarimax import SARIMAX
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
plt.rcParams['figure.figsize'] = (15,10)
from sklearn.metrics import mean_squared_error
import pickle

pd.set_option('display.max_rows', 10)


def prepare_sarimax_data(state_county_data):
    state_county_data = state_county_data.set_index('Date')
    state_county_data = state_county_data.reindex(pd.date_range("2020-03-01", "2020-12-28"), fill_value=0.0)
    return state_county_data

def train_test_split(state_county_data):
    prediction = 'New Cases/100k population'
    region = 'United States'

    #dfjanusa = dfjan[(dfjan['Jurisdiction'] == 'NAT_TOTAL') & (dfjan['CountryName'] == region)][:-1]

    true_value = state_county_data[prediction]
    true_value.index.freq = 'D'
    true_value = true_value.interpolate(method = 'time', limit_direction = 'forward', limit_area = 'inside').fillna(0.0)

    train = true_value[true_value.index < '2020-12-01']
    test = true_value[true_value.index >= '2020-12-01']


    #train-test split-temp
    state_county_data = state_county_data.fillna(method = 'ffill')
    train_df = state_county_data[state_county_data.index < '2020-12-01']
    test_df = state_county_data[(state_county_data.index >= '2020-12-01') & (state_county_data.index < '2021-01-01')]

    train = train_df[prediction]
    test = test_df[prediction]
    true = state_county_data[prediction]
    train.index.freq = 'D'
    test.index.freq = 'D'
    true.index.freq = 'D'
    return train, test, true


def mean_percent_error(y_test, y_hat):
    from math import e
    error = np.abs(y_test - y_hat)
    percent_error = error/(y_test + e)
    mean_percent_error = percent_error.sum() / len(y_test)
    return mean_percent_error


def determine_hyperparameter(train, test):
    print(" ---- Printing train value ----- ")
    print(train.describe())
    cbrt_train = np.cbrt(train)
    #print(cbrt_train)
    flag = True
    test_results = pd.DataFrame(columns = ['p','d','q','P','D','Q','MPE'])

    for p in range(0,4):
        if not flag: break
        for d in range(1,3):
            if not flag: break
            for q in range(0,4):
                if not flag: break
                for P in range(0,4):
                    if not flag: break
                    for D in range(1,3):
                        if not flag: break
                        for Q in range(0,4):
                            try:
                                model = SARIMAX(cbrt_train, order =(p,d,q), seasonal_order = (P,D,Q,7),
                                                freq = 'D')
                                fit_model = model.fit(maxiter = 200, disp = False)
                                yhat = fit_model.forecast(len(test))
                                yhat = yhat**3
                                ind = f'order = ({p},{d},{q}), seasonal_order = ({P},{D},{Q},7)'
                                mpe = mean_percent_error(test,yhat)
                                print(f'trying {ind}, MPE = {mpe}')
                                test_results.loc[ind,'MPE'] = mpe
                                test_results.loc[ind,'MPE'] = mpe
                                test_results.loc[ind,'p'] = p
                                test_results.loc[ind,'d'] = d
                                test_results.loc[ind,'q'] = q
                                test_results.loc[ind,'P'] = P
                                test_results.loc[ind,'D'] = D
                                test_results.loc[ind,'Q'] = Q
                                if mpe <= 2.1:
                                    flag = False
                                    break
                            except Exception as e:
                                print(e)
                                continue

    print('min value :',test_results.min())
    test_results.sort_values(by = 'MPE')
    test_results_filtered = test_results[(test_results['MPE'] > 2.3) & (test_results['MPE'] <= 3.0)]
    row, cols = test_results_filtered.shape
    if row == 0:
        test_results_filtered = test_results[(test_results['MPE'] > 3.1) & (test_results['MPE'] <= 5.0)]
    row, cols = test_results_filtered.shape
    if row == 0:
        test_results.sort_values(by = 'MPE')
        test_results_filtered = test_results

    test_results_filtered.sort_values(by = 'MPE')
    first_row = test_results_filtered.head(1)
    print(first_row)
    p = first_row['p'][0]
    d = first_row['d'][0]
    q = first_row['q'][0]
    P = first_row['P'][0]
    D = first_row['D'][0]
    Q = first_row['Q'][0]


    print('index ',p,d,q,P,D,Q)
    return p,d,q,P,D,Q

def train_SARIMAX(train, test, p,d,q,P,D,Q):
    cbrt_train =  np.cbrt(train)

    model2 = SARIMAX(cbrt_train, order = (p,d,q), seasonal_order = (P,D,Q,7),
                     freq = 'D')
    fit_model2 = model2.fit(maxiter = 200, disp = False)
    yhat = fit_model2.forecast(len(test)+30)**3
    mpe = mean_percent_error(test,yhat)
    print(f'mpe = {mpe}')
    return yhat

def SARIMAX_result_df(train, yhat,state_name, county_name):
    lst = []

    for y in train.keys():
        #print(y)
        row = {}
        row['Date'] = y
        row['Province_State'] = state_name
        row['County Name'] = county_name
        row['New Cases/100k population'] = train[y]
        lst.append(row)
    for y in yhat.keys():
    #print(y)
        row = {}
        row['Date'] = y
        row['Province_State'] = state_name
        row['County Name'] = county_name
        row['New Cases/100k population'] = yhat[y]
        lst.append(row)

        df_estimates = pd.DataFrame(lst)

    return df_estimates


