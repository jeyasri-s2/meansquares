# County Population + FIPS Code:
* US_population_filename = wget.download('https://usafactsstatic.blob.core.windows.net/public/data/covid-19/covid_county_population_usafacts.csv')
* county_population_US = pd.read_csv(US_population_filename,low_memory=False)
* print(county_population_US.shape)
