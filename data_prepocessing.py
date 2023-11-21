import pandas as pd
import os
from scipy.special import boxcox1p
import numpy as np
import requests
import shutil
from sklearn.preprocessing import OneHotEncoder,LabelEncoder,RobustScaler
from sklearn.model_selection import train_test_split

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import pickle
import time

#dataset reference columns
df_ref=pd.read_csv('https://github.com/arifalse/bootcamp_datascience_files/raw/main/column_ref_x_test.csv',nrows=1)

#dform origin
df=pd.read_csv('car_price_prediction.csv')

#clean some of it
df=df[df.Levy!='-']
df['Mileage']=df['Mileage'].str.replace(' km','').astype('int64')
column_form=['Manufacturer','Model','Prod. year','Levy','Category','Leather interior', 'Fuel type',\
             'Engine volume', 'Mileage','Cylinders', 'Gear box type', 'Drive wheels', 'Wheel', 'Color','Airbags']
df=df[column_form]

def get_dtypes() :
    dict_result={}
    for i in df.columns :
        if i in ['Levy','Mileage'] :
            dict_result[i]=str('float64')
        else :
            dict_result[i]=str('object')    
    return dict_result

def get_unique(column) :
    ls_unique=sorted(df[column].unique().tolist())
    if column=='Engine volume' :
        ls_unique.pop(0)

    return ls_unique

def get_min_max(column):
    ls_minmax=[float(df[column].min()),float(df[column].max())]
    return ls_minmax

#### FUNCTIONS FOR DATA PREP
def encoder(df,columns) :

    #load encoder
    list_encoder=[i for i in os.listdir() if str(i).__contains__('encoder_')]
    list_column_from_encoder=[str(i).split('.pkl')[0].split('encoder_')[1] for i in list_encoder]
    dict_encoder={list_column_from_encoder[i]: list_encoder[i] for i in range(len(list_encoder))}

    #loop to encode based on its column
    for col in columns :
        print(col)
        if col in dict_encoder.keys() :
                pkl_file = open(dict_encoder.get(col), 'rb')
                le_encoder = pickle.load(pkl_file)
                pkl_file.close()

                df[col]=le_encoder.transform(df[col].values.tolist())

    return df

def data_preparation(dform,os):

    # Tranform Levy col to replace '-' with 0
    dform['Levy']=dform['Levy'].astype('int64')
    
    # Transform Mileage to numeric/int datatype
    dform['Mileage'] = dform['Mileage'].astype(str).str.replace('km', '')
    dform['Mileage'] = pd.to_numeric(dform['Mileage'], errors='coerce')

    # Transform Engine volume to float and adding Turbo feature
    dform['Turbo'] = dform['Engine volume'].str.contains('Turbo', case=False, na=False)
    dform["Turbo"]=dform["Turbo"].astype('float64')
    
    dform['Engine volume']=dform['Engine volume'].str.replace('Turbo','')
    dform["Engine volume"]=dform["Engine volume"].astype('float64')
        
    #replace value to petrol
    dform['Fuel type'] = dform['Fuel type'].replace(to_replace=r".*Hybrid.*", value='Petrol', regex=True)

    #add column electric source
    dform['Electric source'] = dform['Fuel type'].str.contains('Hybrid', case=False, na=False)
    dform["Electric source"] = dform["Electric source"].astype('float64')

    #Label encoding
    obdata = dform.select_dtypes(include=object)
    numdata = dform.select_dtypes(exclude=object)

    #load encoder
    dfencoded=encoder(obdata,obdata.columns)

    #merge data
    dftest=pd.concat([dfencoded,numdata],axis=1)
    dftest.columns=df_ref.columns
    

#==========================MODELING STAGE==========================#
    
    #load model
    file_model = open('random_forrest_regressor_alpha.pkl', 'rb')
    rfregressor = pickle.load(file_model)
    file_model.close()
  
    #predict new data
    predicted_price=rfregressor.predict(dftest)
    return '$'+str(int(round(predicted_price[0],2)))