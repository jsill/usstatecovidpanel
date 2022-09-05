# usstatecovidpanel

This repository contains code and data for the creation and analysis of a monthly time series (often referred to as a "panel") of U.S. state covid data.  Data is merged from many sources into one csv of monthly values for the sake of creating a dataset which can be used to study the association of various factors with covid and/or all-cause excess death rates.  Data on social distancing policy and behavior, mask mandates, vaccination and boosted rates, temperature and humidity are all included. 

Joe Sill ( jsill at alumni dot caltech dot edu) is the owner of this repository and can be contacted with any questions or suggestions.

Three Jupyter notebooks are included. The notebooks are written in Python3, with R used for many statistical analyses. 

1) WeatherAPI.ipynb downloads and processes historical temperature and relative humidity data from the service WeatherAPI. WeatherAPI is a paid service which currently costs $60/month for a subscription required to download historical data. If you want to download the raw WeatherAPI data yourself (e.g. for a different time period than what is supplied here) you would need to buy a subscription and substitute YOURKEYHERE in the code with your own key.  State monthly average humidity and temperature csvs - with averages weighted by county population- named HumiditiesByState.csv and TemperatureByState.csv derived from the raw WeatherAPI data are included in the OfficialData_downloadedJuly25_2022 folder. These csvs were produced by running WeatherAPI.ipynb. However, the raw WeatherAPI data (downloaded weekly and by county) is not included in this repository since it comes from a paid service and therefore is likely not appropriate for wide distribution. If a individual researcher wants access to the raw historical WeatherAPI data I downloaded, I might be able to supply it as long as that researcher agrees not to distribute it further.

2) DataPreparation.ipynb merges data from many sources and creates the monthly time series csv, panelDataFrame.csv. A ready-to-go copy of panelDataFrame.csv is also included in the repository, for those who wish to run statistical analyses without running DataPreparation.ipynb or getting into the details of data preparation. DataPreparation.ipynb may nonetheless be useful as documentation of how panelDataFrame.csv was produced from original sources.  Downloaded data from various sources (with the exception of raw weather data, as previously noted) is included in the OfficialData_downloadedJuly25_2022 folder for reproducibility. DataPreparation.ipynb reads from that folder. Note that if you were to modify DataPreparation.ipynb and re-run it, it would overwrite panelDataFrame.csv in your local copy of the repository unless you change the name of the csv to be written to disk.

The data sources used are as follows:

a) Excess death data. Source: https://www.cdc.gov/nchs/nvss/vsrr/covid19/excess_deaths.htm

b) Covid case and death data.  Source: https://covid.cdc.gov/covid-data-tracker/#trends_dailycases_select_00

c) Covid vaccination data. Source: https://data.cdc.gov/Vaccinations/COVID-19-Vaccinations-in-the-United-States-Jurisdi/unsk-b7fc

d) Social distancing government policy data. Source: https://www.bsg.ox.ac.uk/research/research-projects/covid-19-government-response-tracker 

e) Social distancing behavior (mobility) data. Source: https://www.google.com/covid19/mobility/ 

f) Mask mandate data. Source: https://statepolicies.com/data/library/

g) Humidity and temperature data. Source: weatherapi.com 

3) StatisticalAnalysis.ipynb studies the lagged association of relative humidity with excess and covid death rates 2 months later, using the data in panelDataFrame.csv and using data from the various other sources as controls. The panelDataFrame.csv file (or a modified version thereof) might potentially be used in the future for other studies which focus on other covid-related variables rather than relative humidity, though. 
