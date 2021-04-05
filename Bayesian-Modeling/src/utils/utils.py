import pandas as pd

from models.data_labeling import label_result
import math

def get_cosine_distance(filename,similar_county_name,base_county_name):
    county_similarity_data = pd.read_csv('../data/'+filename,low_memory=False)
    county_similarity_data_filtered = county_similarity_data[(county_similarity_data['County Name'] == similar_county_name)  & (county_similarity_data['similar_county'] == base_county_name)]
    cosine_distance = county_similarity_data_filtered['cosine_distance'].tolist()[0]
    return cosine_distance


def display_probs(d, labels):
    values = []
    for key, value in d.items():
        print(f'Labels: {key:8} Prevalence: {100*value:.2f}%.')
        values.append(value)

    return values

def compute_bayesian_probability_values(cosine_distance, similar_bayesian_values):
    Bayesian_probability_minimal = (cosine_distance * similar_bayesian_values[0])
    Bayesian_probability_nochange = (cosine_distance * similar_bayesian_values[1])
    Bayesian_probability_widespread = (cosine_distance * similar_bayesian_values[2])

    return Bayesian_probability_minimal,Bayesian_probability_nochange,Bayesian_probability_widespread


def label_real_data(filename,similar_state_name,similar_county_name,population, range1, points, range4):
    all_covid_data = pd.read_csv('../data/'+filename,low_memory=False)
    all_covid_data_filtered = all_covid_data[all_covid_data['Date'] >= '2020-03-01']
    similar_covid_data = all_covid_data_filtered[(all_covid_data_filtered['Province_State'] == similar_state_name)]
    similar_covid_data = similar_covid_data[similar_covid_data['County Name'] == similar_county_name]
    similar_covid_data['New Cases/100k population'] = similar_covid_data['New cases']*100000/ population

    avg_col_idx = similar_covid_data.columns.get_loc("New Cases/100k population")
    print(avg_col_idx)
    similar_covid_data['daily_growth_range'] = similar_covid_data.iloc[:,avg_col_idx].diff().fillna(0)

    labeled_realdata_df = label_result(similar_covid_data,similar_county_name, range1,points,range4)
    return labeled_realdata_df


def mean_percent_error_metric(y, y_bar):
    n = len(y)
    summation = 0
    for i in range (0,n):  #looping through each element of the list
        difference = y[i] - y_bar[i]  #finding the difference between observed and predicted value
        squared_difference = difference**2  #taking square of the differene
        summation = summation + squared_difference  #taking a sum of all the differences
        MSE = summation/n  #dividing summation by
    return MSE

def root_mean_percent_error(y, y_bar):
    n = len(y)
    summation = 0
    for i in range (0,n):  #looping through each element of the list
        difference = y[i] - y_bar[i]  #finding the difference between observed and predicted value
        squared_difference = difference**2  #taking square of the differene
        summation = summation + squared_difference  #taking a sum of all the differences
        MSE = summation/n  #dividing summation by
        RMSE = math.sqrt(MSE)
    return RMSE


