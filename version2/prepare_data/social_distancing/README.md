
# Source: 
* Description: Descartes Labs is releasing mobility statistics (representing the distance a typical member of a given population moves in a day) at the US admin1 (state) and admin2 (county) level. A technical report describing the motivation behind this work with methodology and definitions is available at arxiv.org/pdf/2003.14228.pdf. We intend to update the data in this repository regularly.
Note: Data for 2020-04-20, 2020-05-29, 2020-10-08 and 2020-12-11 through 2020-12-18 did not meet quality control standards, and was not released.

* Link: https://github.com/descarteslabs/DL-COVID-19

# Social Distancing Metric:
* socialdistancing_url = 'https://raw.githubusercontent.com/descarteslabs/DL-COVID-19/master/DL-us-mobility-daterow.csv'
* socialdistancing_file = wget.download(socialdistancing_url)
* socialdistancing_data = pd.read_csv(socialdistancing_file,low_memory=False)
* socialdistancing_data.tail(2)
