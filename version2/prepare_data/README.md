# Data Sources:

* **Combined data:** from merging all the listed datasets-
> 1. Social Distancing
> 2. Google mobility data,
> 3. Covid Cases- John Hopkins university
> 4. Population Density
> 5. Mask data for rule


*  **Inertia Data:** Merging Social Distancing Inertia (Maryland data) and Covid data integration


## County Population + FIPS Code:
* US_population_filename = wget.download('https://usafactsstatic.blob.core.windows.net/public/data/covid-19/covid_county_population_usafacts.csv')
* county_population_US = pd.read_csv(US_population_filename,low_memory=False)
* print(county_population_US.shape)


## COVID Data Source:
* Description: John Hopkins university updates data every day hence we are pulling from repository directly
* US Confirmed url :https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv
* US deaths url: https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv

## Data:
* urls = ['https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv',
        'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv']
* [wget.download(url) for url in urls]
* confirmed_US = pd.read_csv('time_series_covid19_confirmed_US.csv',low_memory=False)
* death_US = pd.read_csv('time_series_covid19_deaths_US.csv',low_memory=False)


## Google Mobility Data:
* google_data_url = 'https://raw.githubusercontent.com/ActiveConclusion/COVID19_mobility/master/google_reports/mobility_report_US.csv'
* google_filename = wget.download(google_data_url)
* google_mobility_data = pd.read_csv(google_filename,low_memory=False)
* google_mobility_data.head(2)



## Maryland Data:
* Source: https://data.covid.umd.edu/
* Drive Link: https://drive.google.com/drive/u/1/folders/1tB49AJOPg2dE1kvxDY-ntJ3puUAVSo75

## Mask Data

* mask_rule_data = pd.read_csv('/content/drive/Shared drives/CMPE 295- Master Project/Covid19-data/mask_rule.csv',low_memory=False)


## Source:
* Description: Descartes Labs is releasing mobility statistics (representing the distance a typical member of a given population moves in a day) at the US admin1 (state) and admin2 (county) level. A technical report describing the motivation behind this work with methodology and definitions is available at arxiv.org/pdf/2003.14228.pdf. We intend to update the data in this repository regularly.
Note: Data for 2020-04-20, 2020-05-29, 2020-10-08 and 2020-12-11 through 2020-12-18 did not meet quality control standards, and was not released.

* Link: https://github.com/descarteslabs/DL-COVID-19

## Social Distancing Metric:
* socialdistancing_url = 'https://raw.githubusercontent.com/descarteslabs/DL-COVID-19/master/DL-us-mobility-daterow.csv'
* socialdistancing_file = wget.download(socialdistancing_url)
* socialdistancing_data = pd.read_csv(socialdistancing_file,low_memory=False)
* socialdistancing_data.tail(2)

## files in google drive
 ( Note: only Developers has access to this folder path)
 
 **Social Distancing data :**
* /content/drive/Shared drives/CMPE 295- Master Project/projectdata-2021/`<<state>>`_SocialDistancingDataJan10.csv -> eg., NY_SocialDistancingDataJan10.csv, CA_SocialDistancingDataJan10.csv, TX_SocialDistancingDataJan10.csv

 **COVID-19 and population data :**

* /content/drive/Shared drives/CMPE 295- Master Project/projectdata-2021/`<<state>>`_CovidDataJan10.csv -> Eg., CA_CovidDataJan10.csv, NY_CovidDataJan10.csv, TX_CovidDataJan10.csv

**Google Mobility Data:**

* /content/drive/Shared drives/CMPE 295- Master Project/projectdata-2021/`<<state>>`_GoogleMobilityDataJan10.csv -> Eg., NY_GoogleMobilityDataJan10.csv, CA_GoogleMobilityDataJan10.csv, TX_GoogleMobilityDataJan10.csv


