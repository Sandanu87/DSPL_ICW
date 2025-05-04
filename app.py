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
st.write("This dashboard provides an interactive insights of crime statistics in Sri Lanka. This allows users to explore crime trends, geographical distribution and overall summaries which enables data driven decision making for government authorities. ")
st.write("Here's a inital glance at the data:")
st.dataframe(df.head())

print(px.__version__)

#summary stats
st.write("Here's a summary of the data:")
st.dataframe(df.describe())

#Crime trends overtime
st.header("1. Crime Rate Trends Over Time")
selected_crime_categories = st.multiselect("Select Crime Categories", options=df['Crime Category'].unique(), default=['Murder', 'Theft of Property Including praedial produce over Rs . 5000 / & cycle cattle theft Irrespective of their value'])

if not selected_crime_categories:
    st.warning("Please select at least one crime category to display the chart.")
else:
    try:
        df_melted = df.melt(id_vars=['District', 'Crime Category', 'Population'], value_vars=['2010', '2011', '2012'], var_name='Year', value_name='Cases')

        df_filtered = df_melted[df_melted['Crime Category'].isin(selected_crime_categories)]

        df_filtered['Year'] = pd.to_numeric(df_filtered['Year'])

        df_filtered['Crime Rate'] = (df_filtered['Cases'] / df_filtered['Population']) * 100000

        fig = px.line(df_filtered,
                      x='Year',
                      y='Crime Rate',
                      color='Crime Category',
                      hover_data=['Year', 'Crime Category', 'District', 'Crime Rate'],
                      title='Crime Rate Trends Over Time')
        fig.update_layout(width=800, height=500)
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"An error occurred while creating the chart: {e}")