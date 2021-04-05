import pandas as pd
import numpy as np
from models.sarimax_modeling import prepare_sarimax_data
from models.sarimax_modeling import train_test_split
from models.sarimax_modeling import determine_hyperparameter
from models.sarimax_modeling import train_SARIMAX
from models.sarimax_modeling import SARIMAX_result_df
from models.data_labeling import label_result

from models.data_labeling import identify_ranges
from models.Bayesian_inference import determine_c_array,run_bayesian_inference

from datetime import datetime
import seaborn as sns
import matplotlib.pyplot as plt

# Initialize variable
from utils.utils import get_cosine_distance, display_probs, compute_bayesian_probability_values
from utils.utils import label_real_data,mean_percent_error_metric,root_mean_percent_error
from sklearn.metrics import confusion_matrix

prefix = '../data/'
similarity_file = 'OR_SuperData_With_SimilarityScore_Mar26.csv'

superset_filename = 'AllStates_Superset_dataset_Mar26.csv'
covid_alldata = 'alldatasets_Mar26.csv'
# Determine parameters for each state



def load_data():
    data = pd.read_csv(prefix+superset_filename,low_memory=False)
    data['Date'] =  pd.to_datetime(data['Date'], format='%Y-%m-%d')

    county_data = data[(data['County Name'] == similar_county_name)]

    county_data = county_data[(data['Province_State'] == similar_state_name)]

    county_data = county_data[(county_data['Date'] >= '2020-03-01') & (county_data['Date'] <= '2020-12-28')]
    columns = ['Date','New Cases/100k population']
    return county_data[columns]

def get_population():
    data = pd.read_csv(prefix+superset_filename,low_memory=False)
    county_data = data[(data['County Name'] == similar_county_name) & (data['Province_State'] == similar_state_name)]
    county_data = county_data[(county_data['Date'] >= '2020-03-01') & (county_data['Date'] <= '2020-12-28')]
    return county_data['Population'].values[0]



if __name__ == '__main__':
    result_df = pd.DataFrame(columns = ['similar_state', 'base_state', 'similar_county','base_county',
                                       'minimal_probability','nochange_probability','widespread_probability',
                                       'real_minimal','real_nochange','real_widespread','MSE','RMSE','confusion_matrix'])


    data_files = pd.read_csv('../data/testing.csv',low_memory=False)
    print(data_files.head(3))
    for index, row in data_files.iterrows():

        similar_county_name = row['similar_county_name']
        similar_state_name = row['similar_state_name']
        similar_state_code = row['similar_state_code']
        similar_county_code = row['similar_county_code']
        base_state_name = row['base_state_name']
        base_county_name = row['base_county_name']
        base_state_code = row['base_state_code']
        base_county_code = row['base_county_code']
        print(similar_county_name,similar_state_name)

        #print(prepare_sarimax_data(data))
        data = load_data()
        print(data.tail(2))
        sarimax_data = prepare_sarimax_data(data)
        print(sarimax_data.head())
        train_df, test_df, true_df= train_test_split(sarimax_data)
        #p,d,q,P,D,Q = determine_hyperparameter(train_df, test_df)
        p,d,q,P,D,Q = 0,1,1,0,1,1

        yhat = train_SARIMAX(train_df, test_df,p,d,q,P,D,Q )
        result_df = SARIMAX_result_df(train_df, yhat, similar_state_name, similar_county_name)
        print(result_df)
        filename = similar_state_code+'_'+similar_county_code+'_SARIMAX_estimates'+datetime.now().strftime("%b%d")+'.csv'
        # Saving SARIMAX result
        result_df.to_csv('../output/'+filename,index=False)

        range1,points,range4 = identify_ranges(data)
        print(range1,points,range4)
        avg_col_idx = result_df.columns.get_loc("New Cases/100k population")
        print(avg_col_idx)
        result_df['daily_growth_range'] = result_df.iloc[:,avg_col_idx].diff().fillna(0)

        labeled_sarimax_df = label_result(result_df,similar_county_name, range1,points,range4)
        labeled_sarimax_filtered = labeled_sarimax_df[(labeled_sarimax_df['Date'] > '2020-12-29') & (labeled_sarimax_df['Date'] <= '2021-01-05')]
        c = determine_c_array(labeled_sarimax_filtered)
        labels = ['minimal', 'No Change', 'widespread']
        trace_df = run_bayesian_inference(c, labels)
        output_filename = similar_state_code+'_'+similar_county_code+'_Bayesian_inference_'+datetime.now().strftime("%b%d")+'.csv'
        # Saving Bayesian inference result
        trace_df.to_csv('../output/'+output_filename,index=False)

        cosine_distance = get_cosine_distance(similarity_file,similar_county_name,base_county_name)
        pvals = trace_df.iloc[:, :3].mean(axis = 0)


        similar_bayesian_values = display_probs(dict(zip(labels, pvals)))

        Bayesian_probability_minimal,Bayesian_probability_nochange,Bayesian_probability_widespread = compute_bayesian_probability_values(cosine_distance, similar_bayesian_values)

        population = get_population()
        label_real_data_df = label_real_data(covid_alldata,similar_state_name,similar_county_name,population, range1, points, range4)
        label_real_data_verify_df = label_real_data_df[(label_real_data_df['Date'] > '2020-12-29') & (label_real_data_df['Date'] <= '2021-01-05')]

        minimal_count = 0
        widespread_count = 0
        nochange_count = 0

        for s in label_real_data_verify_df.growth_label_estimate:
            #print(s)
            if s == 'widespread':
                widespread_count +=1
            elif s == 'minimal':
                minimal_count+=1
            elif s == 'nochange':
                nochange_count+=1

        length = len(label_real_data_verify_df.growth_label_estimate)
        minimal = (minimal_count / length)
        widespread = (widespread_count / length)

        nochange = (nochange_count / length)
        #print(minimal, nochange, widespread)
        y_pred = [Bayesian_probability_minimal,Bayesian_probability_nochange,Bayesian_probability_widespread]
        y_test = [minimal,nochange,widespread]
        MSE = mean_percent_error_metric(y_test, y_pred)
        RMSE = root_mean_percent_error(y_test, y_pred)
        #print(confusion_matrix(y_test, y_pred, labels=labels))
        confusion_matrix_arr = confusion_matrix(y_test, y_pred, labels=labels)

        print("MSE ", MSE)
        print("RMSE" ,RMSE)
        print("confusion_matrix_arr ",confusion_matrix_arr)
        final_df = pd.DataFrame(columns = ['index','similar_state', 'base_state', 'similar_county','base_county',
                                            'minimal_probability','nochange_probability','widespread_probability',
                                            'real_minimal','real_nochange','real_widespread','MSE','RMSE','confusion_matrix'])


        final_df['index'] = row['id']
        final_df['similar_state'] = similar_state_name
        final_df['base_state'] = base_state_name
        final_df['similar_county'] = similar_county_name
        final_df['base_county'] = base_county_name
        final_df['minimal_probability'] = Bayesian_probability_minimal
        final_df['nochange_probability'] = Bayesian_probability_nochange
        final_df['widespread_probability'] = Bayesian_probability_widespread
        final_df['real_minimal'] = minimal
        final_df['real_nochange'] = nochange
        final_df['real_widespread'] = widespread
        final_df['MSE'] = MSE
        final_df['RMSE'] = RMSE
        final_df['confusion_matrix'] = confusion_matrix_arr

        print(final_df)
        result_df = result_df.append(final_df, ignore_index=True)
        break
    #
    print(result_df.shape)
    result_df.to_csv('../output/allregions_bayesian_metrics.csv')

