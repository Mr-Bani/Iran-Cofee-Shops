# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
from sql_connector import *
from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode
import altair as alt
import numpy as np
import pydeck as pdk
import matplotlib.pyplot as plt
import seaborn as sns

sql = sql_connector(user="user_group2", password="sBTdgyAxvrEs_group2", host="45.139.10.138",port=80, database="group2")

st.set_page_config(layout="wide", page_title="Iran Coffee Shops", page_icon=":coffee:")
df = sql.get_all_tables()
st.title("Iran Coffee Shops")

row1_1, row1_2 = st.columns((2, 10))

sns.set_theme(style="dark")
st.header("Coffee Shops of each city")
fig, ax = plt.subplots(figsize=(20, 10))
bar = sns.barplot(x=df["city"].value_counts().index, y=df["city"].value_counts().values, ax=ax)
bar.set_ylim(0, 150)
bar.set_xticklabels(bar.get_xticklabels(), rotation=45, horizontalalignment='right')
bar.set_ylabel("Number of Coffee Shops")
bar.set_xlabel("City")
st.pyplot(fig);








st.title("Map of Coffee Shops")
@st.experimental_singleton
def load_data():
    data = sql.get_one_table("cafe_location")
    return data


def map(data, lat, lon, zoom):
    st.write(
        pdk.Deck(
            map_style="mapbox://styles/mapbox/light-v9",
            initial_view_state={
                "latitude": lat,
                "longitude": lon,
                "zoom": zoom,
                "pitch": 50,
            },
            layers=[
                pdk.Layer(
                    'ScatterplotLayer',
                    data=data,
                    get_position=["longitude", "latitude"],
                    radius=300,
                    elevation_scale=2,
                    elevation_range=[0, 100],
                    auto_highlight=True,
                    get_radius=100,
                    get_fill_color='[180, 0, 200, 200]',
                    pickable=True,
                    extruded=True,
                ),
            ],
        )
    )


@st.experimental_memo
def mpoint(lat, lon):
    return (np.average(lat), np.average(lon))

data = load_data()

midpoint = mpoint(data["latitude"], data["longitude"])

map(data, midpoint[0], midpoint[1], 12)





st.header("Table of Coffee Shops")



def aggrid_interactive_table(df: pd.DataFrame):
    options = GridOptionsBuilder.from_dataframe(
        df,header_name="Coffee Shops list", enableRowGroup=True, enableValue=True, enablePivot=True
    )


    options.configure_side_bar()

    options.configure_selection("single")
    selection = AgGrid(
        df,
        enable_enterprise_modules=True,
        gridOptions=options.build(),
        update_mode=GridUpdateMode.MODEL_CHANGED,
        allow_unsafe_jscode=True,
    )

    return selection

cafe = sql.get_all_tables()

selection = aggrid_interactive_table(df=cafe)
