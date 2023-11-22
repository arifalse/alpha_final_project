import streamlit as st
import pandas as pd 
from data_prepocessing import *

#width form
css='''
<style>
    section.main > div {max-width:80rem}
    </style>
'''
st.markdown(css, unsafe_allow_html=True)

#title
st.markdown("<h1 style='text-align: center; color: white;'>CAR PRICE PREDICTION</h1>", unsafe_allow_html=True)

#column for dataset form
column_form=['Manufacturer','Model','Prod. year','Levy','Category','Leather interior', 'Fuel type',\
             'Engine volume', 'Mileage','Cylinders', 'Gear box type', 'Drive wheels', 'Wheel', 'Color','Airbags']

#Form construction
with st.form(key='columns_in_form'):
    c1, c2, c3, c4 = st.columns(4,gap='large')
    with c1:
        Manufacturer=st.selectbox('Manufacturer',get_unique('Manufacturer'))
        Model=st.selectbox('Model',get_unique('Model'))
        Production_year=st.selectbox('Production year',get_unique('Prod. year'))
        Engine_volume=st.selectbox('Engine volume',get_unique('Engine volume'))

    with c2:
        Cylinders=st.selectbox('Cylinders',get_unique('Cylinders'))
        Category=st.selectbox('Category',get_unique('Category'))
        Levy=st.slider('Levy',float(get_min_max('Levy')[0]),float(get_min_max('Levy')[1]))
        Mileage=st.slider('Mileage',float(get_min_max('Mileage')[0]),float(600000))

    with c3:
        Fuel_type=st.selectbox('Fuel type',get_unique('Fuel type'))
        Color=st.selectbox('Color',get_unique('Color'))
        Drive_wheels=st.selectbox('Drive wheels',get_unique('Drive wheels'))
        Gear_box_type=st.selectbox('Gear box type',get_unique('Gear box type'))

    with c4:
        Wheel=st.selectbox('Wheel',get_unique('Wheel'))
        Airbags=st.selectbox('Airbags',get_unique('Airbags'))
        Leather_interior=st.selectbox('Leather interior',get_unique('Leather interior'))

    submitButton = st.form_submit_button(label = 'Predict',type='primary')
    if submitButton:
        
        
        data=[Manufacturer,Model,Production_year,Levy,Category,Leather_interior, Fuel_type,\
             Engine_volume, Mileage,Cylinders,Gear_box_type,Drive_wheels,Wheel,Color,Airbags]

        data_form=pd.DataFrame([data],columns=column_form)
              
        data_form=data_preparation(data_form,os)

        st.divider()

        st.subheader(f':green[The Price Prediction for this Car is :] {data_form}',divider='rainbow')
        