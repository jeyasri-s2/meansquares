# Masters Project Dashboard

# Installation
## Install Virtual Enviornment
`pip3 install virtualenv`

## Create and activate Virtual Enviornment
`python3 -m venv env`

### Apple / Linux
`source env/bin/activate`

### Windows 10
`env/Scripts/activate.bat`

## Install required packages
`pip install -r requirements.txt`

### Windows 10 and Linux
Some additional Steps might be required. Please select a version based on your version of python
`python3 --version`

#### Step 1: Download the required files
- [Geospatial Data Abstraction(GDAL)](https://www.lfd.uci.edu/~gohlke/pythonlibs/#gdal)
- [Fiona](https://www.lfd.uci.edu/~gohlke/pythonlibs/#fiona) 

#### Step 2: Install the files
- `pip install {path/to/gdal.whl}`
- `pip install {path/to/fiona.whl}`

#### Step 3: Install all required packages
`pip install -r requirements.txt`

# To run project
`streamlit run COVID\ Dashboard.py`

# Understanding dataset

Preprocessing_All_Data.ipynb contains the dataformat and geopandas shp file used in the dashboard

dashboard_data_preparation.ipynb contains the code used to forecast the number of cases in the future
