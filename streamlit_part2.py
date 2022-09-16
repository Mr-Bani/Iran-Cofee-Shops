import streamlit as st
import requests
import pandas as pd
import numpy as np
from datetime import datetime
from datetime import time
from sql_connector import *
import haversine as hs
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt



user= 'user_group2'
password = 'sBTdgyAxvrEs_group2'
db = 'group2'
host = '45.139.10.138'
port = '80'

sql = sql_connector(host,user,password,db,port)

data = sql.get_all_tables()

df_f = sql.get_one_table('cafe_features')
df_f.drop('cafe_id',axis=1,inplace=True)

location = sql.get_one_table('cafe_location')

# max_feature = data.copy()
# max_feature['sum_features'] = np.sum(df1.loc[:,],axis=1)


# data['start'] = pd.to_datetime(pd.Timestamp('today').normalize() + data['work_start']).dt.time
# data['end'] = pd.to_datetime(pd.Timestamp('today').normalize() + data['work_end']).dt.time

data['start'] = pd.to_datetime(data['work_start'],format="%H:%M").dt.time
data['end'] = pd.to_datetime(data['work_end'],format="%H:%M").dt.time
data.loc[data['end'] == min(data['end']),'end'] = time(23,59,59,999999)

data.drop(columns=['type'],axis=1)



max_feature = data.copy()
max_feature['sum_features'] = np.sum(df_f.loc[:,],axis=1)
max_feature['rating'] = np.mean(max_feature.loc[:,'food_quality':'environment'],axis=1)


fig_box = px.box(data_frame=max_feature,x='rating',color='city',
            title="BoxPlot for Rating Among Different Cities",
            labels={'rating':"Rating"})
st.plotly_chart(fig_box)

fig_hist = px.histogram(data_frame=max_feature,x='rating',color='cost',barmode='group',
                   title="Histogram of Rating Along with Cost Level",
                   labels={"rating":"Rating","count":"Count Of Cafes","cost":"Cost Level"})

st.plotly_chart(fig_hist)
fig_heatmap , ax = plt.subplots(figsize=[6,3])
df_corr = max_feature[['cost','food_quality','cost_value','environment','service_quality','sum_features']].copy()
sns.heatmap(df_corr.corr(),annot=True,ax=ax)

st.pyplot(fig_heatmap)

df_quality = max_feature[['city','food_quality','cost_value','service_quality','environment']].copy()
df_quality = df_quality.groupby(by='city').mean()
df_quality = df_quality.sort_values(by='food_quality',ascending=False)

city_plot_selection = st.multiselect("Choose Cities",
                                data['city'].unique(),
                                None)
if city_plot_selection != []:
    mask_quality = df_quality.index.isin(city_plot_selection)
    df_quality = df_quality.loc[mask_quality]
fig_quality = px.bar(data_frame=df_quality,x=df_quality.index,y=df_quality.columns,barmode='group'
                     , title='Mean Of Rated Quality Features For Each City',
                     labels={'city':'City','value':'Mean','variable':"Rated Features"})

st.plotly_chart(fig_quality)


feature_percentage = max_feature[['city','hookah','internet','delivery','smoking','open_space','live_music','parking','pos']].copy()
feature_percentage = feature_percentage.groupby(by='city').mean() * 100

fig_percentage = px.bar(data_frame=feature_percentage,x=feature_percentage.index,y=feature_percentage.columns,
                        title="Percentage Of Each Extra Feature Among All Cities (Stacked BarChart)",
                        labels={'value':'Percentage','city':'City','variable':'Extra Features'})

st.plotly_chart(fig_percentage)

city_selection = st.multiselect("Which cities do you want?",
                                data['city'].unique(),
                                None)


def city_filter(df_city):
    mask = df_city['city'].isin(city_selection)
    if city_selection == []:
        return df_city
    else:
        return df_city[mask]
df1 = city_filter(data)

cost_level = st.multiselect(
    "Choose your cost level",
    np.sort(data['cost'].unique()),
    None
)

def cost_filter(df_cost):
    mask = df_cost['cost'].isin(cost_level)
    if cost_level == []:
        return df_cost
    else:
        return df_cost[mask]

df2 = cost_filter(df1)
what_features = st.multiselect(
    "What are your favorite features?!",
    df_f.columns,
    None
)

def feature_filter(df_feature):
    if what_features == []:
        return df_feature
    else:
        for col in what_features:
            mask = df_feature[col] == 1
            df_feature = df_feature.loc[mask]
        return df_feature

df3 = feature_filter(df2)

time_preference = st.radio(
    "Select your time prference",
    ["Nothing",'Choose your desired time','Which cafes are open right now'])

def time_filter(df_time):
    now = datetime.now()
    if time_preference == 'Nothing':
        return df_time

    elif time_preference == 'Choose your desired time':
        time_range = st.slider(
            "What times suit you?",
            value=(time(6,0,0), time(23,59,0)))
        mask_time = (df_time['start'] <= time_range[0]) & (df_time['end'] >= time_range[1])
        return df_time.loc[mask_time]

    else:
        st.write("Now Time is: ", now.time())
        mask_time = (df_time['start'] <= now.time()) & (df_time['end'] >= now.time())
        return df_time.loc[mask_time]

df4 = time_filter(df3)
checking = st.checkbox('Do you wanna check your distance to cafes?!')
if checking:
    lat_entry = st.number_input("Insert your latitude:",format='%.7f',value=35.7545502)
    long_entry = st.number_input("Insert your longitude:",format='%.7f',value=51.2575889)

    def distance_filter(df_distance):
        df_distance['distance (KM)'] = location.apply(lambda row: hs.haversine([row['latitude'],row['longitude']],[lat_entry,long_entry]),axis=1)

        return df_distance

desired_columns = ['cafe_name', 'city', 'cost', 'phone_number', 'cafe_address','work_start','work_end']

if checking:
    desired_columns += ['distance (KM)']
    df5 = distance_filter(df4)
else:
    df5 = df4



st.write("Number Of Cafes: ", len(df5))
st.dataframe(df5[desired_columns])
