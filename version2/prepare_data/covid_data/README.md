
# COVID Data Source:
* Description: John Hopkins university updates data every day hence we are pulling from repository directly
* US Confirmed url :https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv
* US deaths url: https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv

# Data:
* urls = ['https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv',
        'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv']
* [wget.download(url) for url in urls]
* confirmed_US = pd.read_csv('time_series_covid19_confirmed_US.csv',low_memory=False)
* death_US = pd.read_csv('time_series_covid19_deaths_US.csv',low_memory=False)
