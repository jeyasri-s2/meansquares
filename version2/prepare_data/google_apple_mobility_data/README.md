
# Google Mobility Data:
* google_data_url = 'https://raw.githubusercontent.com/ActiveConclusion/COVID19_mobility/master/google_reports/mobility_report_US.csv'
* google_filename = wget.download(google_data_url)
* google_mobility_data = pd.read_csv(google_filename,low_memory=False)
* google_mobility_data.head(2)

# Apple Mobility Data:
* apple_report_url = 'https://raw.githubusercontent.com/ActiveConclusion/COVID19_mobility/master/apple_reports/apple_mobility_report_US.csv'
* apple_filename = wget.download(apple_report_url)
* apple_mobility_data = pd.read_csv(apple_filename,low_memory=False)
* apple_mobility_data.tail(2)

# Combined Mobility Data:
* CA_mobility_data = pd.merge(CA_GoogleMobility_data,CA_AppleMobility_data,how='outer' ,on=['state','county','date'])
* CA_mobility_data.shape
