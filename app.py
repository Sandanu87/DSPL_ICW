import seaborn as sns
import streamlit as st
import pandas as pd
import plotly.express as px

try:
    df = pd.read_csv("crime_data_2010_1012.csv")
except FileNotFoundError:
    st.error("Could not find the data file.")
    st.stop()

df['District'] = df['District'].astype(str)

#inital view of the dataset
st.title("Sri Lankan Crime Statistics Dashboard")
st.write("This dashboard provides an interactive visualization of crime statistics in Sri Lanka.")
st.write("Here's a first look at the data:")
st.dataframe(df.head())

