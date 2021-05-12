"""
# COVID-19 Dashboard
"""

import json
import pathlib
from typing import Optional

import geopandas as gpd
import pandas as pd
import numpy as np
import streamlit as st
from bokeh.models import ColorBar, GeoJSONDataSource, LinearColorMapper
from bokeh.palettes import brewer  # pylint: disable=no-name-in-module https://docs.bokeh.org/en/latest/docs/reference/palettes.html
from bokeh.plotting import figure
import datetime
import time

# Set page to open in wide layout
st.set_page_config(page_title="COVID-19 Dashboard",page_icon="🧊",layout="wide",initial_sidebar_state="expanded",)

# Set Dataset file and US Shape File
FILE_DIR = pathlib.Path.cwd() / ""
SHAPEFILE = FILE_DIR / "UScounties/UScounties.shp"
COVID_DATASET_FILE = FILE_DIR / "UScounties/data_labeled_Apr23.csv"
COUNTY_FILE = FILE_DIR / "UScounties/county_fips_master.csv"
CSS_FILE = FILE_DIR / "css/styles.css"

# Streamlit local download file
STREAMLIT_STATIC_PATH = pathlib.Path(st.__path__[0]) / 'static'

DOWNLOADS_PATH = (STREAMLIT_STATIC_PATH / "downloads")
if not DOWNLOADS_PATH.is_dir():
    DOWNLOADS_PATH.mkdir()

INFO = ""
# Dashboard class
#
#A Dashboard showing the New Cases/100k population and Forecasted cases within the lower 48 States in the United States
#
class CovidDashboard:

    def __init__(
        self,
        shape_data: Optional[gpd.geodataframe.GeoDataFrame] = None,
        covid_data_set: Optional[pd.DataFrame] = None,
    ):

        if not shape_data:
            self.shape_data = self.get_shape_data()
        else:
            self.shape_data = shape_data

        if not covid_data_set:
            self.covid_data_set = self.get_covid_dataset()
            self.covid_data_set['date_range'] = self.covid_data_set['week'].apply(lambda x:datetime.datetime.strptime(f'{2021}-W{int(x )- 1}-1', "%Y-W%W-%w").date())

        self.dataset_name = "COVID 'New Cases/100k population' Dataset"
        #min = self.covid_data_set['date_range'].min()
        #max = self.covid_data_set['date_range'].max()
        min = datetime.date(2021, 1, 25)
        max = datetime.date(2021, 4, 26)
        self.week_range = (min, max)
        self.date_range = min
        self.category = "New Cases/100k population"

    def map_plot(self):
        """The Bokeh Map"""
        print("map_plot ", self.date_range)

        return self._map_plot(self.dataset_name, self.date_range,self.category)

    def _map_plot(self, name: str, date_range: object,category: str):
        print("_map_plot ",date_range)
        if name and date_range:
            shape_data, key = self.get_covid_data(
                self.covid_data_set, self.shape_data, name=name, date_range=date_range, key=category
            )
            print('_map_plot ', shape_data.shape, key)

            return self.get_map_plot(shape_data, key, key)
        return None

    @staticmethod
    @st.cache
    def get_shape_data() -> gpd.geodataframe.GeoDataFrame:
        """Load the shape data from the lower 48 states within the United States"""
        shape_data = gpd.read_file(SHAPEFILE)
        print("Tiger Data Shape:", shape_data.shape)
        shape_data['FIPS'] = shape_data['FIPS'].apply(lambda x: int(x))

        return shape_data

    @staticmethod
    @st.cache
    def get_covid_dataset() -> pd.DataFrame:
        """The DataFrame of data from COVID Forecasted Data"""
        data = pd.read_csv(COVID_DATASET_FILE)
        data['month'] = pd.DatetimeIndex(data['Date']).month
        data['week'] = pd.DatetimeIndex(data['Date']).week
        data['Spread Category'] = pd.Categorical(data['growth_label_estimate']).codes

        df = data.pipe(lambda x: x.assign(month=x.week)).reset_index(drop=True).pivot_table(values='New Cases/100k population', columns='week', index='FIPS', aggfunc='mean').rename_axis(None, axis=1).reset_index()
        weekly_data = (df.melt(id_vars='FIPS', value_vars=data['week'].unique()).rename(columns={"variable": "week", "value": "New Cases/100k population"}))

        df_labeled = data.pipe(lambda x: x.assign(month=x.week)).reset_index(drop=True).pivot_table(values='Spread Category', columns='week', index='FIPS', aggfunc='last').rename_axis(None, axis=1).reset_index()
        weekly_data_labeled = (df_labeled.melt(id_vars='FIPS', value_vars=data['week'].unique()).rename(columns={"variable": "week", "value": "Spread Category"}))

        weekly_data_merged = weekly_data.merge(weekly_data_labeled, left_on=["FIPS", "week"], right_on=["FIPS", "week"], how="left")
        weekly_data_merged['date_range'] = weekly_data_merged['week'].apply(lambda x:datetime.datetime.strptime(f'{2021}-W{int(x)- 1}-1', "%Y-W%W-%w").date())

        county_data = pd.read_csv(COUNTY_FILE)
        county_data_filtered = county_data[['fips','county_name']]
        weekly_data_merged_updated = weekly_data_merged.merge(county_data_filtered, left_on=['FIPS'], right_on=['fips'], how='left')
        print('weekly_data_merged_updated cols: ',weekly_data_merged_updated.columns)
        return weekly_data_merged_updated
    
    @staticmethod
    @st.cache
    def get_covid_dataset_sidebar(self, selection) -> pd.DataFrame:
        """The DataFrame of data from COVID"""
        date_range = self.date_range
        year = date_range.year
        month = date_range.month
        date_val = date_range.day

        covid_data_set = self.covid_data_set[self.covid_data_set["date_range"] == datetime.date(year, month, date_val)]
        data = covid_data_set.sort_values(by=[selection])
        unique = data['FIPS'].unique().tolist()[0:10]
        #county_names = pd.read_csv('https://raw.githubusercontent.com/kjhealy/fips-codes/master/county_fips_master.csv', encoding='cp1252')
        list =[]
        for county in unique:
            value = data[data['fips']==county].county_name.values
            list.append(value.tolist()[0])

        return list

    @classmethod
    def get_covid_data(  # pylint: disable=too-many-arguments
        cls,
        covid_data_set: pd.DataFrame,
        shape_data: gpd.geodataframe.GeoDataFrame,
        name: str,
        week: Optional[int] = None,
        date_range : Optional[object] = None,
        key: Optional[str] = None,
    ) -> gpd.geodataframe.GeoDataFrame:

        print(date_range)
        covid_data_set = cls.get_covid_dataset()
        print('covid_data_set shape in get_covid_data before : ',covid_data_set.shape)


        if date_range is not None:
            #datetime.date(2021, 1, 25)
            print('date_range in filter: ',date_range)
            year = date_range.year
            month = date_range.month
            date_val = date_range.day

            covid_data_set = covid_data_set[covid_data_set["date_range"] == datetime.date(year, month, date_val)]
            print('covid_data_set shape in get_covid_data after : ',covid_data_set.shape)

        merged = shape_data.merge(covid_data_set, left_on="FIPS", right_on="FIPS", how="left")
        key = key

        merged = merged[(merged['STATE_NAME'] != 'Alaska') & (merged['STATE_NAME'] != 'Hawaii')]
        merged[key] = merged[key].fillna(0)
        print("Merged Data Shape after na check:", merged.shape)

        return merged, key

    @staticmethod
    def to_geo_json_data_source(data: gpd.geodataframe.GeoDataFrame) -> GeoJSONDataSource:
        """Convert the data to a GeoJSONDataSource

        Args:
            data (gpd.geodataframe.GeoDataFrame): The data

        Returns:
            GeoJSONDataSource: The resulting GeoJson Data
        """
        #print(data.columns)
        data_filtered = data[['NAME', 'STATE_NAME', 'STATE_FIPS', 'CNTY_FIPS', 'FIPS', 'geometry',
                            'week', 'New Cases/100k population', 'Spread Category']]
        json_data = json.dumps(json.loads(data_filtered.to_json()))
        return GeoJSONDataSource(geojson=json_data)

    @classmethod
    def get_map_plot(
        cls,
        shape_data: gpd.geodataframe.GeoDataFrame,
        value_column: Optional[str] = None,
        title: str = "",
    ):
        """Plot GeoDataFrame as a map


        """

        print('shape_data shape: ',shape_data.shape)
        geosource = cls.to_geo_json_data_source(shape_data)
        palette = brewer["GnBu"][8]
        if value_column == 'Spread Category':
            palette = brewer["OrRd"][8]

        palette = palette[::-1]
        vals = shape_data[value_column]
        color_mapper = LinearColorMapper(palette=palette, low=vals.min(), high=vals.max())
        color_bar = ColorBar(
            color_mapper=color_mapper,
            label_standoff=8,
            height=20,
            location=(0, 0),
            orientation="horizontal",
        )

        TOOLTIPS = [
            ('FIPS', '@FIPS'),
            ('New Cases/100k population', '@{New Cases/100k population}'),
            ('Spread Category', '@{Spread Category}')
        ]

        plot = figure(title=title, sizing_mode="stretch_width", tooltips=TOOLTIPS)
        plot.xgrid.grid_line_color = None
        plot.ygrid.grid_line_color = None
        plot.patches(
            "xs",
            "ys",
            source=geosource,
            fill_alpha=1,
            line_width=0.5,
            line_color="black",
            fill_color={"field": value_column, "transform": color_mapper},
        )
        plot.add_layout(color_bar, "below")
        plot.toolbar.logo = None
        return plot

    def view(self):
        # Markdown Format
        st.markdown('<style>' + open(CSS_FILE).read() + '</style>', unsafe_allow_html=True)

        st.markdown(__doc__)
        # Sidebar
        st.sidebar.title("COVID-19 Dashboard")

        selection = st.sidebar.radio("Select a category",('Forecasted Cases', 'Spread Category'))
        print("selection ",selection)
        if(selection == "Forecasted Cases"):
            key = "New Cases/100k population"
            self.category = key
            self.week = max(self.covid_data_set['week']) - 2


        if(selection == 'Spread Category'):
            key='Spread Category'
            self.category = key
            self.week = max(self.covid_data_set['week']) - 2

        # Map dashboard
        self.date_range = st.slider(
            "Week starting",
            min_value=self.week_range[0],
            max_value=self.week_range[1],
            value=self.date_range,
            format="MM/DD",
            step=datetime.timedelta(days=7)
        )
        st.write("Displaying data for week starting ",str(self.date_range.month)+'/'+str(self.date_range.day)+'/'+str(self.date_range.year))
        st.bokeh_chart(self.map_plot())

        top_counties = self.get_covid_dataset_sidebar(self, key)
        st.sidebar.write("Top Counties for week")
        for i in top_counties:
            st.sidebar.text(i)



CovidDashboard().view()
