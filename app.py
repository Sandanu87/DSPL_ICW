import seaborn as sns
import streamlit as st
import pandas as pd
import plotly.express as px
import json
import plotly.graph_objects as go

try:
    df = pd.read_csv("crime_data_2010_1012.csv")
except FileNotFoundError:
    st.error("Could not find the data file.")
    st.stop()

df['District'] = df['District'].astype(str)

# shortening district names
district_mapping = {
    'Badulla (Badulla & Bandarawela )': 'Badulla',
    'Colombo (Colombo South, North, Central) Mt. Laviniya, Nugegoda': 'Colombo',
    'Galle (Galle/Elpitiya)': 'Galle',
    'Gampaha (Kelaniya/Gampha/Negombo Div)': 'Gampaha',
    'Hambanthota (Tangalle )': 'Hambantota',
    'Jaffna(Jaffna, KKS)': 'Jaffna',
    'Kalutara (Kalutara,Panadura)': 'Kalutara',
    'Kandy (Kandy, Gampola)': 'Kandy',
    'Mannar ':'Mannar',
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
    'Theft of Property including praedial produce over Rs. 5000/ & cycle cattle theft  irrrespective of their value ': 'Theft > 5000',
    'Cruelty to Children & sexual  exploitation of children ':'Child Abuse',
    'Cheating/Misappropriation C.B. Trust over Rs.100,000/=': 'Cheating/Misappropriation',
    'Possession of  Automatic or  Repeater Shot Guns': 'Possession of Arms',
    'Offences under the  Poisons, Opium & Dangerous Drugs Ord. Quantity  as  indicated in Circular NO. 1540/2000': 'Use of dangerous drugs',
    'Theft of Property including praedial produce over Rs. 5000/ & cycle cattle theft  irrrespective of their value ': 'Theft <= 5000'}
df['Crime Category'] = df['Crime Category'].replace(crime_category_mapping)

#inital view of the dataset
st.title("Sri Lankan Crime Statistics Dashboard")
st.write("This dashboard provides an interactive insights of crime statistics in Sri Lanka. This allows users to explore crime trends, geographical distribution and overall summaries which enables data driven decision making for government authorities. ")
st.write("Here's a inital glance at the data:")
st.dataframe(df.head())

#summary stats
st.write("Here's a summary of the data:")
st.dataframe(df.describe())

#crime trends overtime by district
st.header("1. Crime Trends Over Time by District")
try:
    df_melted = df.melt(id_vars=['District'], value_vars=['2010', '2011', '2012'], var_name='Year', value_name='Total Crimes')
    df_melted['Year'] = pd.to_numeric(df_melted['Year']) 

    selected_district = st.selectbox("Select a District", df_melted['District'].unique())

    district_data = df_melted[df_melted['District'] == selected_district]

    fig = px.bar(district_data, x='Year', y='Total Crimes',
                  title=f'Crime Trends in {selected_district}',
                  labels={'Year': 'Year', 'Total Crimes': 'Total Crimes'}) 
    st.plotly_chart(fig, use_container_width=True) 

except Exception as e:
    st.error(f"An error occurred: {e}")

#Crime trends overtime
st.header("2. Crime Rate Trends Over Time")
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
st.header("3. Geographical Distribution of Crime")
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
    fig.update_layout(width=1200, height=600, legend=dict(font=dict(size=10)))
    st.plotly_chart(fig, use_container_width=True)
except Exception as e:
        st.error(f"An error occurred: {e}")

#geographical distribution of crime by map
st.header("4. Geographical Distribution of Total Crime Percentage by Year")
selected_year = st.selectbox("Select Year", options=['2010', '2011', '2012'], key="year_selector_1")
selected_year = int(selected_year)

try:
    district_corrections = {
    'Mulathivu': 'Mullaitivu',
    'Mulllativu': 'Mullaitivu',}
    df['District'] = df['District'].replace(district_corrections)

    df['District'] = df['District'].str.strip().str.title() + " District"

    df['Crime Rate'] = (df[str(selected_year)] / df['Population']) * 100000

    with open("geoBoundaries-LKA-ADM2.geojson", "r") as f:
        sri_lanka_map = json.load(f)

    district_crime_counts = df.groupby('District')[str(selected_year)].sum().reset_index()
    district_crime_counts = district_crime_counts.rename(columns={str(selected_year): 'Total Crimes'})
    total_crimes = district_crime_counts['Total Crimes'].sum()
    district_crime_counts['Crime Percentage'] = (district_crime_counts['Total Crimes'] / total_crimes) * 100

    MAPBOX_TOKEN = "pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndjZ3bWl3N3gifQ._7RTFeGZ0dY-NU8U6GI2wQ"
    map_center = {"lat": 7.8731, "lon": 80.7718}

    fig = go.Figure(go.Choroplethmapbox(
        geojson=sri_lanka_map,
        locations=district_crime_counts['District'],
        z=district_crime_counts['Crime Percentage'],
        featureidkey="properties.shapeName",
        colorscale="Reds",
        colorbar_title="Crime %",
        marker_opacity=0.6,
        marker_line_width=1,
        hovertext=district_crime_counts['District'],
        hoverinfo="text+z"
    ))

    fig.update_layout(
        mapbox_style="carto-positron",
        mapbox_zoom=6.2,
        mapbox_center=map_center,
        mapbox_accesstoken=MAPBOX_TOKEN,
        margin={"r": 0, "t": 30, "l": 0, "b": 0},
        height=600,
        title=f"Crime Distribution in Sri Lanka - {selected_year}"
    )

    st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"An error occurred: {e}")

#population vs crime count
st.header("5.Crime vs. Population by Category")
df.columns = df.columns.str.strip()

df["Population"] = pd.to_numeric(df["Population"], errors='coerce')
df["Crimes Over the Years"] = pd.to_numeric(df["Crimes Over the Years"], errors='coerce')
df["Crime Percentage"] = pd.to_numeric(df["Crime Percentage"], errors='coerce')

df = df.dropna(subset=["Population", "Crimes Over the Years", "Crime Percentage", "Crime Category"])

fig = px.scatter(
    df,
    x="Population",
    y="Crimes Over the Years",
    color="Crime Category",
    size="Crime Percentage",
    hover_data=["District"],
    title="Scatter Plot: Population vs. Crime, Colored by Crime Category",)

st.plotly_chart(fig)

#top and bottom 5 
st.header("6. Top and Bottom 5 Districts by Crime Rate")
selected_year_rate = st.selectbox("Select Year", options=['2010', '2011', '2012'], key="year_rate")
selected_year_rate = int(selected_year_rate)

try:
    df_rate = df.copy()
    df_rate['Crime Rate'] = (df_rate[str(selected_year_rate)] / df_rate['Population']) * 100000
    df_rate = df_rate[['District', 'Crime Rate']].sort_values(by='Crime Rate')

    top_5_districts = df_rate.head(5)
    bottom_5_districts = df_rate.tail(5)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader(f"Top 5 Districts in {selected_year_rate}")
        st.dataframe(top_5_districts, height=200)

    with col2:
        st.subheader(f"Bottom 5 Districts in {selected_year_rate}")
        st.dataframe(bottom_5_districts, height=200)

except Exception as e:
    st.error(f"An error occurred: {e}")

#animated Chart over time
st.header("7. Animated Crime Trends by District")
try:
    df_melted_animated = df.melt(id_vars=['District', 'Population'], value_vars=['2010', '2011', '2012'], var_name='Year',
                                 value_name='Cases')
    df_melted_animated['Year'] = pd.to_numeric(
        df_melted_animated['Year'])

    df_melted_animated['Crime Rate'] = (df_melted_animated['Cases'] / df_melted_animated['Population']) * 100000

    fig_animated = px.bar(df_melted_animated,
                             x='District',
                             y='Crime Rate',
                             color='District',
                             animation_frame='Year',
                             range_y=[0, df_melted_animated['Crime Rate'].max() * 1.1],
                             title='Annual Crime Rate per 100,000 Population by District',
                             labels={'Year': 'Year', 'Crime Rate': 'Crime Rate (per 100,000)'})

    fig_animated.update_layout(
        transition=dict(duration=300, easing="cubic-in-out"),
        height=700
    )

    st.plotly_chart(fig_animated, use_container_width=True)
except Exception as e:
    st.error(f"An error occurred: {e}")