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

# shortening district names
district_mapping = {
    'Badulla (Badulla & Bandarawela)': 'Badulla',
    'Colombo (Colombo South, North, Central) Mt. Laviniya, Nugegoda': 'Colombo',
    'Galle (Galle/Elpitiya)': 'Galle',
    'Gampaha (Kelaniya/Gampha/Negombo Div)': 'Gampaha',
    'Hambanthota (Tangalle )': 'Hambantota',
    'Jaffna(Jaffna, KKS)': 'Jaffna',
    'Kalutara (Kalutara,Panadura)': 'Kalutara',
    'Kandy (Kandy, Gampola)': 'Kandy',
    'Kegalle (Kegalle, Sithawakapura0': 'Kegalle',
    'Kilinochchi (Kilinochchi, Mankulam )': 'Kilinochchi',
    'Kurunegala (Kurunegala, Kuliyapitiya, Nikaweratiya )': 'Kurunegala',

    'Nuwara Eliya (Hatton, Nuwara Eliya )':'Nuwara Eliya',
    'Puttlam (Puttlam, Chilaw )': 'Puttalam',
    'Trincomalee (Kantale, Trincomalee )': 'Trincomalee',}
df['District'] = df['District'].replace(district_mapping)

#shotening crime names
crime_category_mapping = {
    'Abduction / Kidnapping': 'Abduction/Kidnap',
    'Theft of Property Including praedial produce over Rs . 5000 / & cycle cattle theft Irrespective of their value': 'Theft > 5000',
    'All other thefts': 'Other Thefts',
    'Assaults': 'Assault',
    'Attempted Murder': 'Attempted Murder',
    'Bribery': 'Bribery',
    'Burglary': 'Burglary',
    'Cheating': 'Cheating',
    'Criminal Trespass': 'Criminal Trespass',
    'Damaging Private Property': 'Damage Property',
    'Extortion': 'Extortion',
    'Grave Robbery': 'Grave Robbery',
    'Homicide': 'Homicide',
    'House Breaking': 'House Breaking',
    'Human trafficking': 'Human trafficking',
    'Murder': 'Murder',
    'Other': 'Other',
    'Other offences against': 'Other offences against',
    'Possession of Ganja': 'Possession of Ganja',
    'Rape': 'Rape',
    'Rioting': 'Rioting',
    'Robbery': 'Robbery',
    'Sexual Harassment': 'Sexual Harassment',
    'Theft of Motor Vehicle': 'Vehicle Theft',
    'Theft of Property Including praedial produce Rs. 5000/- and below': 'Theft <= 5000'}
df['Crime Category'] = df['Crime Category'].replace(crime_category_mapping)

#inital view of the dataset
st.title("Sri Lankan Crime Statistics Dashboard")
st.write("This dashboard provides an interactive insights of crime statistics in Sri Lanka. This allows users to explore crime trends, geographical distribution and overall summaries which enables data driven decision making for government authorities. ")
st.write("Here's a inital glance at the data:")
st.dataframe(df.head())

#summary stats
st.write("Here's a summary of the data:")
st.dataframe(df.describe())

#Crime trends overtime
st.header("1. Crime Rate Trends Over Time")
options = df['Crime Category'].unique().tolist()
default_values = [
    val for val in [
        'Murder',
        'Theft of Property Including praedial produce over Rs . 5000 / & cycle cattle theft Irrespective of their value'] if val in options]
selected_crime_categories = st.multiselect("Select Crime Categories",
    options=options,
    default=default_values)

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

#geographical distribution of crime
st.header("2. Geographical Distribution of Crime")
selected_year = st.selectbox("Select Year", options=['2010', '2011', '2012'], index=0)
selected_year = int(selected_year)

try:
    df['Crime Rate'] = (df[str(selected_year)] / df['Population']) * 100000
    fig = px.bar(df,
                 x='District',
                 y='Crime Rate',
                 color='Crime Category',
                 hover_data=['District', 'Crime Category', 'Crime Rate'],
                 title=f'Geographical Distribution of Crime in {selected_year}')
    fig.update_layout(width=800, height=500, legend=dict(font=dict(size=10)))
    st.plotly_chart(fig, use_container_width=True)
except Exception as e:
        st.error(f"An error occurred: {e}")