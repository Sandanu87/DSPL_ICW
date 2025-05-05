import streamlit as st
import seaborn
import pandas as pd
import plotly.express as px
import json
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(layout="wide")   

try:
    df = pd.read_csv("crime_data_2010_1012.csv")
except FileNotFoundError:
    st.error("Could not find the data file.")
    st.stop()
df['District'] = df['District'].astype(str)

st.title("Sri Lankan Crime Statistics Dashboard")
st.write("This dashboard provides an interactive insights of crime statistics in Sri Lanka. This allows users to explore crime trends, geographical distribution and overall summaries which enables data driven decision making for government authorities. ")

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

#Navigation bar
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select a Page", [
    "Basic Overview",
    "Crime Rate Trends",
    "Geographical Distribution",
    "Advanced Insights",])

#inital view of the dataset
if page == "Basic Overview":
    st.header("Initial overview of the data")
    st.write("Here's a inital glance at the data:")
    st.dataframe(df.head())

    total_population = df[['District', 'Population']].drop_duplicates()['Population'].sum()
    total_crime_categories = df["Crime Category"].nunique()
    total_districts = df["District"].nunique()
    total_2011 = df['2011'].sum()
    total_2010 = df['2010'].sum()
    total_2012 = df['2012'].sum()

    # Display stats
    st.header("Key Statistics")
    col1, col2, col3 = st.columns(3) 
    col1.markdown(
        f"""
        <div style="background-color: #e0f7fa; border-left: 4px solid #00bcd4; padding: 10px; border-radius: 5px; margin-bottom: 10px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);">
            <p style="font-size: 16px; color: #00897b;"><strong>Total Population:</strong> {total_population:,}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    col2.markdown(
        f"""
        <div style="background-color: #e0f7fa; border-left: 4px solid #00bcd4; padding: 10px; border-radius: 5px; margin-bottom: 10px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);">
            <p style="font-size: 16px; color: #00897b;"><strong>Total Crime Categories:</strong> {total_crime_categories}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    col3.markdown(
        f"""
        <div style="background-color: #e0f7fa; border-left: 4px solid #00bcd4; padding: 10px; border-radius: 5px; margin-bottom: 10px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);">
            <p style="font-size: 16px; color: #00897b;"><strong>Total Districts:</strong> {total_districts}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col4, col5, col6 = st.columns(3)
    col4.markdown(
        f"""
        <div style="background-color: #e0f7fa; border-left: 4px solid #00bcd4; padding: 10px; border-radius: 5px; margin-bottom: 10px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);">
            <p style="font-size: 16px; color: #00897b;"><strong>Total Crimes in 2010:</strong> {total_2010:,}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    col5.markdown(
        f"""
         <div style="background-color: #e0f7fa; border-left: 4px solid #00bcd4; padding: 10px; border-radius: 5px; margin-bottom: 10px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);">
            <p style="font-size: 16px; color: #00897b;"><strong>Total Crimes in 2011:</strong> {total_2011:,}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    col6.markdown(
        f"""
         <div style="background-color: #e0f7fa; border-left: 4px solid #00bcd4; padding: 10px; border-radius: 5px; margin-bottom: 10px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);">
            <p style="font-size: 16px; color: #00897b;"><strong>Total Crimes in 2012:</strong> {total_2012:,}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    #summary stats
    st.write("Here's a summary of the data:")
    st.dataframe(df.describe())

#crime trends overtime by district
elif page == "Crime Rate Trends":
    st.header("Crime Trends Over Time by District")
    try:
        df_melted = df.melt(
            id_vars=['District'],
            value_vars=['2010', '2011', '2012'],
            var_name='Year',
            value_name='Total Crimes'
        )
        df_melted['Year'] = pd.to_numeric(df_melted['Year'])

        selected_district = st.selectbox("Select a District", sorted(df_melted['District'].unique()))

        district_data = df_melted[df_melted['District'] == selected_district]
        district_yearly = district_data.groupby('Year', as_index=False)['Total Crimes'].sum()

        fig = px.line(
            district_yearly,
            x='Year',
            y='Total Crimes',
            title=f'Crime Trends in {selected_district}',
            labels={'Year': 'Year', 'Total Crimes': 'Total Crimes'}
        )
        fig.update_traces(mode='lines+markers')
        fig.update_layout(width=800, height=500)

        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"An error occurred: {e}")

    #crime trends overtime
    st.header("Crime Rate Trends Over Time")

    options = df['Crime Category'].unique().tolist()
    selected_crime_categories = st.multiselect("Select Crime Categories", options=options)

    if not selected_crime_categories:
        st.warning("Please select at least one crime category to display the chart.")
    else:
        try:
            df_melted = df.melt(
                id_vars=['District', 'Crime Category', 'Population'],
                value_vars=['2010', '2011', '2012'],
                var_name='Year',
                value_name='Cases')
            
            df_filtered = df_melted[df_melted['Crime Category'].isin(selected_crime_categories)]

            df_filtered['Year'] = pd.to_numeric(df_filtered['Year'])

            df_grouped = df_filtered.groupby(['Year', 'Crime Category'], as_index=False).agg({
                'Cases': 'sum',
                'Population': 'sum'})

            df_grouped = df_grouped[df_grouped['Population'] > 0]

            df_grouped['Crime Rate'] = (df_grouped['Cases'] / df_grouped['Population']) * 100000

            fig = px.line(
                df_grouped,
                x='Year',
                y='Crime Rate',
                color='Crime Category',
                hover_data=['Year', 'Crime Category', 'Crime Rate'],
                title='Crime Rate Trends Over Time')
            
            fig.update_layout(width=800, height=500)

            st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error(f"An error occurred while creating the chart: {e}")
    
    #top and bottom 5 
    st.header("Top and Bottom 5 Districts by Crime Rate")
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

#geographical distribution of crime
elif page == "Geographical Distribution":
    st.header("Geographical Distribution of Crime")

    selected_year = st.selectbox("Select Year", options=['2010', '2011', '2012'], index=0)
    selected_year = int(selected_year)

    crime_categories = df['Crime Category'].unique().tolist()
    selected_crime = st.selectbox("Select Crime Category", options=crime_categories)

    try:
        district_corrections = {
            'Mulathivu': 'Mullaitivu',
            'Mulllativu': 'Mullaitivu',
            'Kilinochi': 'Kilinochchi',
            'Killinochchi': 'Kilinochchi'
        }
        df['District'] = df['District'].replace(district_corrections)

        filtered_df = df[df['Crime Category'] == selected_crime].copy()
        filtered_df['Crime Rate'] = (filtered_df[str(selected_year)] / filtered_df['Population']) * 100000

        all_districts = df['District'].unique()
        base_df = pd.DataFrame({'District': all_districts})
        merged_df = base_df.merge(filtered_df[['District', 'Crime Rate']], on='District', how='left')
        merged_df['Crime Rate'] = merged_df['Crime Rate'].fillna(0)

        fig = px.bar(
            merged_df,
            x='District',
            y='Crime Rate',
            color='District',
            hover_data=['District', 'Crime Rate'],
            title=f'Geographical Distribution of {selected_crime} in {selected_year}'
        )

        fig.update_layout(width=1200, height=600, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"An error occurred: {e}")


#geographical distribution of crime by map
    st.header("Geographical Distribution of Total Crime Percentage by Year")
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
            hoverinfo="text+z"))

        fig.update_layout(
            mapbox_style="carto-positron",
            mapbox_zoom=6.2,
            mapbox_center=map_center,
            mapbox_accesstoken=MAPBOX_TOKEN,
            margin={"r": 0, "t": 30, "l": 0, "b": 0},
            height=600,
            title=f"Crime Distribution in Sri Lanka - {selected_year}")

        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"An error occurred: {e}")

#population vs crime count
elif page == "Advanced Insights":
    st.header("Crime vs. Population by Category")
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

    #population vs crime rate
    st.header("Crime Rate vs Population Over Time by District")
    try:
        df_melted = df.melt(
            id_vars=['District', 'Crime Category', 'Population'],
            value_vars=['2010', '2011', '2012'],
            var_name='Year',
            value_name='Cases'
        )
        df_melted['Year'] = pd.to_numeric(df_melted['Year'])
        df_melted['Crime Rate'] = (df_melted['Cases'] / df_melted['Population']) * 100000

        selected_district = st.selectbox("Select a District", df_melted['District'].unique())

        district_data = df_melted[df_melted['District'] == selected_district]

        grouped = district_data.groupby('Year').agg({
            'Cases': 'sum',
            'Population': 'mean' }).reset_index()

        grouped['Crime Rate'] = (grouped['Cases'] / grouped['Population']) * 100000

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=grouped['Year'],
            y=grouped['Crime Rate'],
            mode='lines+markers',
            name='Crime Rate (per 100,000)',
            line=dict(color='firebrick')))

        fig.add_trace(go.Scatter(
            x=grouped['Year'],
            y=grouped['Population'],
            mode='lines+markers',
            name='Population',
            yaxis='y2',
            line=dict(color='royalblue')))

        fig.update_layout(
            title=f'Crime Rate vs Population Over Time in {selected_district}',
            xaxis=dict(title='Year'),
            yaxis=dict(title='Crime Rate (per 100,000)', color='firebrick'),
            yaxis2=dict(
                title='Population',
                overlaying='y',
                side='right',
                color='royalblue'),
            width=800,
            height=500)

        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"An error occurred: {e}")


    #pie charts to  show portions
    st.header("Crime Occurrences by District for Selected Crime Category")

    try:
        selected_category = st.selectbox("Select a Crime Category", df['Crime Category'].unique(), key="crime_category_pie_chart")

        df_category = df[df['Crime Category'] == selected_category]

        years = ['2010', '2011', '2012']

        fig = make_subplots(rows=1, cols=3, specs=[[{'type':'domain'}]*3],
                            subplot_titles=[f"Year {year}" for year in years])

        for i, year in enumerate(years):
            fig.add_trace(
                go.Pie(
                    labels=df_category['District'],
                    values=df_category[year],
                    name=f"Year {year}",
                    textinfo='percent+label',
                    hole=0.4
                ),
                row=1, col=i+1)

        fig.update_layout(
            title_text=f"Occurrences of '{selected_category}' Crime Across Districts (2010–2012)",
            showlegend=False,
            width=1000,
            height=600)
        
        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"An error occurred: {e}")
