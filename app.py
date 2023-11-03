import streamlit as st
import pandas as pd
import preprocessor,helper
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.figure_factory as ff


df = pd.read_csv('Billionaires.csv')
df = preprocessor.preprocess(df)
st.sidebar.title("Billionaires Data Analysis")
st.sidebar.image("billion.png")

x = st.sidebar.radio("Select an option", ('Total Billionaires by Country', 'Country Wise Analysis', 'Visualization Plots', 'Billionaires by Industry', 'Industry Wise Analysis', 'Country wise Billionaires'))


if x == 'Total Billionaires by Country':

    country_list = df['country'].unique().tolist()
    country_list.insert(0, 'Overall')

    selected_country = st.selectbox("Select a country ", country_list)
    billionaires_counts = helper.countrywise_billionaires(df, selected_country)
    if selected_country == 'Overall':
        st.title("1. Overall Billionaires in the world")
    if selected_country != 'Overall':
        st.title("1. Total billionaires in " + selected_country)
    st.table(billionaires_counts)

    st.title('2. Billionaires vs Country')
    billionaires_by_country = df.groupby('country')['Billionaires'].count().reset_index()
    fig = px.line(billionaires_by_country, x="country", y="Billionaires", title='Billionaires by country', height=500, width=700)
    fig.update_traces(line=dict(color='green'))
    st.plotly_chart(fig)

    st.title('3. AgeGroup VS Billionaires')
    df['AgeGroup'] = pd.cut(df['age'], bins=[0, 30, 40, 50, 60, 70, 80, 90],
                            labels=['<30', '30-40', '40-50', '50-60', '60-70', '70-80', '80+'])
    billionaires_by_age = df.groupby(['country', 'AgeGroup'])['Billionaires'].count().reset_index()
    # Define a custom color map for age groups
    color_map = {'<30': 'blue', '30-40': 'green', '40-50': 'purple', '50-60': 'orange', '60-70': 'red','70-80': 'magenta', '80+': 'cyan'}
    fig = px.line(billionaires_by_age, x="country", y="Billionaires", color="AgeGroup", title='AgeGroup VS Billionaires', height=600, width=780,color_discrete_map=color_map)
    st.plotly_chart(fig)


if x == 'Country Wise Analysis':

    country_list = df['country'].unique().tolist()
    country_list.insert(0, 'Overall')

    selected_country = st.selectbox("Select a country ", country_list)
    billionaires_counts = helper.countrywise_billionaires(df, selected_country)
    if selected_country == 'Overall':
        st.title("1. Overall Billionaires in the world")
    if selected_country != 'Overall':
        st.title("1. Total billionaires in " + selected_country)
    st.table(billionaires_counts)


    st.title("2. Distribution of Billionares (Bar Plot)")
    country_df = df['country'].value_counts().reset_index()
    country_df.columns = ['country', 'Billionaires']
    fig = px.bar(country_df, x='country', y='Billionaires', title='Number of Billionaires in Each country',color='country',
                 labels={'country': 'Country', 'Billionaires': 'Number of Billionaires'}, height=500, width=800)
    st.plotly_chart(fig)


    st.title("3. Distribution of Billionares (Pie chart)")
    country_df = df['country'].value_counts().reset_index()
    country_df.columns = ['country', 'Billionaires']
    fig = px.pie(country_df, names='country', values='Billionaires', title='Distribution of Billionaires by Industry', height=700)
    st.plotly_chart(fig)


    st.title('4. Billionaires by Country')
    custom_width = 800
    custom_height = 600
    x_data = df.groupby(['country'])['Billionaires'].count().reset_index()
    fig = px.scatter_geo(
        x_data,
        locations="country",
        locationmode="country names",
        hover_name="country",
        size="Billionaires",
        projection="natural earth",
        title="Billionaires by Country (Scatter Geo)",
        width=custom_width,
        height=custom_height,
        color="country"
    )
    st.plotly_chart(fig)


    st.title('5. Line Geo')
    custom_width = 800
    custom_height = 600
    fig = px.line_geo(
        x_data,
        locations="country",
        locationmode="country names",
        color="Billionaires",
        hover_name="country",
        projection="orthographic",
        title="Billionaires by Country (Line Geo)",
        width=custom_width,
        height=custom_height,
    )
    # Set the center and rotation of the map
    fig.update_geos(projection_rotation_lon=60, projection_rotation_lat=60)
    st.plotly_chart(fig)


    st.title('6. Choropleth Map')
    custom_width = 800
    custom_height = 600
    fig = px.choropleth(
        x_data,
        locations="country",
        locationmode="country names",
        color="Billionaires",
        hover_name="country",
        color_continuous_scale=px.colors.sequential.Plasma,
        title="Billionaires by Country (Choropleth Map)",
        width=custom_width,
        height=custom_height,
    )
    st.plotly_chart(fig)


    st.title('7. Billionaires Age Distribution by Country')
    grouped_data = df.groupby(['country', 'age'])['Billionaires'].count().reset_index()
    # Create a list of histograms, one for each country
    hist_data = []
    group_labels = []
    for country in grouped_data['country'].unique():
        age_data = grouped_data[grouped_data['country'] == country]['age']
        hist_data.append(age_data)
        group_labels.append(country)
    # Create a distribution plot
    fig = px.histogram(df, x="age", color="country", nbins=20, title="No of Billionaires in each AgeGroup by Country",height=700,width=820)
    st.plotly_chart(fig)


    st.title('8. Age vs Billionaires')
    # Create a sidebar to control the number of bins
    st.set_option('deprecation.showPyplotGlobalUse', False)
    num_bins = st.slider('Number of Bins', min_value=5, max_value=50, value=20)
    # Create a dynamic distplot
    sns.set(style="whitegrid")
    plt.figure(figsize=(8, 4))
    sns.distplot(helper.hello(df)['age'].dropna(), kde=False, bins=num_bins, color="blue")
    plt.title('Distribution of Billionaires Age')
    plt.xlabel('Age')
    plt.ylabel('Count')
    st.pyplot()


    st.title("9. Age VS Billionaires in Each country")
    famous_countries = ['France', 'United States', 'Mexico', 'India', 'Spain', 'China',
                        'Canada', 'Germany', 'Switzerland', 'Belgium', 'Hong Kong', 'Taiwan', 'Turkey', 'Argentina',
                        'Austria', 'Japan', 'United Kingdom', 'Australia', 'Indonesia', 'Philippines',
                        'United Arab Emirates', 'Russia', 'Brazil', 'Malaysia', 'South Korea', 'Netherlands',
                        'Thailand', 'Singapore', 'Israel', 'Italy', 'South Africa', 'Sweden', 'Monaco'
                        ]
    fig = ff.create_distplot([df[df['country'] == country]['age'].dropna() for country in famous_countries],famous_countries, show_hist=False, show_rug=False)
    fig.update_layout(title_text='Age VS Billionaires in Each country')
    st.plotly_chart(fig)

    st.title('10. AgeGroup VS Billionaires')
    df['AgeGroup'] = pd.cut(df['age'], bins=[0, 30, 40, 50, 60, 70, 80, 90],
                            labels=['<30', '30-40', '40-50', '50-60', '60-70', '70-80', '80+'])
    billionaires_by_age = df.groupby(['country', 'AgeGroup'])['Billionaires'].count().reset_index()
    # Define a custom color map for age groups
    color_map = {'<30': 'blue', '30-40': 'green', '40-50': 'purple', '50-60': 'orange', '60-70': 'red','70-80': 'magenta', '80+': 'cyan'}

    fig = px.line(billionaires_by_age, x="country", y="Billionaires", color="AgeGroup", title='AgeGroup VS Billionaires', height=600, width=780,color_discrete_map=color_map)
    st.plotly_chart(fig)



if x == 'Visualization Plots':

    st.title("1. Bar Plot")
    country_df = df['country'].value_counts().reset_index()
    country_df.columns = ['country', 'Billionaires']
    fig = px.bar(country_df, x='country', y='Billionaires', title='Number of Billionaires in Each country',color='country',
                 labels={'country': 'Country', 'Billionaires': 'Number of Billionaires'}, height=500, width=800)
    st.plotly_chart(fig)

    st.title("2. Pie chart")
    country_df = df['country'].value_counts().reset_index()
    country_df.columns = ['country', 'Billionaires']
    fig = px.pie(country_df, names='country', values='Billionaires', title='Distribution of Billionaires by Industry',
                 height=700)
    st.plotly_chart(fig)

    st.title('3. Billionaires by Country')
    custom_width = 800
    custom_height = 600
    x_data = df.groupby(['country'])['Billionaires'].count().reset_index()
    fig = px.scatter_geo(
        x_data,
        locations="country",
        locationmode="country names",
        hover_name="country",
        size="Billionaires",
        projection="natural earth",
        title="Billionaires by Country (Scatter Geo)",
        width=custom_width,
        height=custom_height,
        color="country"
    )
    st.plotly_chart(fig)

    st.title('4. Line Geo')
    custom_width = 800
    custom_height = 600
    fig = px.line_geo(
        x_data,
        locations="country",
        locationmode="country names",
        color="Billionaires",
        hover_name="country",
        projection="orthographic",
        title="Billionaires by Country (Line Geo)",
        width=custom_width,
        height=custom_height,
    )
    # Set the center and rotation of the map
    fig.update_geos(projection_rotation_lon=60, projection_rotation_lat=60)
    st.plotly_chart(fig)

    st.title('5. Choropleth Map')
    custom_width = 800
    custom_height = 600
    fig = px.choropleth(
        x_data,
        locations="country",
        locationmode="country names",
        color="Billionaires",
        hover_name="country",
        color_continuous_scale=px.colors.sequential.Plasma,
        title="Billionaires by Country (Choropleth Map)",
        width=custom_width,
        height=custom_height,
    )
    st.plotly_chart(fig)

    st.title('6. Billionaires Age Distribution by Country')
    grouped_data = df.groupby(['country', 'age'])['Billionaires'].count().reset_index()
    # Create a list of histograms, one for each country
    hist_data = []
    group_labels = []
    for country in grouped_data['country'].unique():
        age_data = grouped_data[grouped_data['country'] == country]['age']
        hist_data.append(age_data)
        group_labels.append(country)
    # Create a distribution plot
    fig = px.histogram(df, x="age", color="country", nbins=20, title="Billionaires Age Distribution by Country")
    st.plotly_chart(fig)

    st.title('7. Age vs Billionaires')
    # Create a sidebar to control the number of bins
    st.set_option('deprecation.showPyplotGlobalUse', False)
    num_bins = st.slider('Number of Bins', min_value=5, max_value=50, value=20)
    # Create a dynamic distplot
    sns.set(style="whitegrid")
    plt.figure(figsize=(8, 4))
    sns.distplot(helper.hello(df)['age'].dropna(), kde=False, bins=num_bins, color="blue")
    plt.title('Distribution of Billionaires Age')
    plt.xlabel('Age')
    plt.ylabel('Count')
    st.pyplot()

    st.title("8. Age VS Billionaires in Each country")
    famous_countries = ['France', 'United States', 'Mexico', 'India', 'Spain', 'China',
                        'Canada', 'Germany', 'Switzerland', 'Belgium', 'Hong Kong', 'Taiwan', 'Turkey', 'Argentina',
                        'Austria', 'Japan', 'United Kingdom', 'Australia', 'Indonesia', 'Philippines',
                        'United Arab Emirates', 'Russia', 'Brazil', 'Malaysia', 'South Korea', 'Netherlands',
                        'Thailand', 'Singapore', 'Israel', 'Italy', 'South Africa', 'Sweden', 'Monaco'
                        ]
    fig = ff.create_distplot([df[df['country'] == country]['age'].dropna() for country in famous_countries],
                             famous_countries, show_hist=False, show_rug=False)
    fig.update_layout(title_text='Age VS Billionaires in Each country')
    st.plotly_chart(fig)

    st.title('9. AgeGroup VS Billionaires')
    df['AgeGroup'] = pd.cut(df['age'], bins=[0, 30, 40, 50, 60, 70, 80, 90],
                            labels=['<30', '30-40', '40-50', '50-60', '60-70', '70-80', '80+'])
    billionaires_by_age = df.groupby(['country', 'AgeGroup'])['Billionaires'].count().reset_index()
    # Define a custom color map for age groups
    color_map = {'<30': 'blue', '30-40': 'green', '40-50': 'purple', '50-60': 'orange', '60-70': 'red',
                 '70-80': 'magenta', '80+': 'cyan'}

    fig = px.line(billionaires_by_age, x="country", y="Billionaires", color="AgeGroup",
                  title='AgeGroup VS Billionaires', height=600, width=780, color_discrete_map=color_map)
    st.plotly_chart(fig)

    st.title('10. Billionaires vs Country')
    billionaires_by_country = df.groupby('country')['Billionaires'].count().reset_index()
    fig = px.line(billionaires_by_country, x="country", y="Billionaires", title='Billionaires by country', height=500,
                  width=700)
    fig.update_traces(line=dict(color='green'))
    st.plotly_chart(fig)



if x == 'Billionaires by Industry':
    industry_list = df['industries'].unique().tolist()
    industry_list.insert(0, 'Overall')

    selected_industry = st.selectbox("Select an Industry ", industry_list)
    billionaires_counts = helper.industrywise_billionaires(df, selected_industry)
    if selected_industry == 'Overall':
        st.title("1. Overall Billionaires in each Industry")
    if selected_industry != 'Overall':
        st.title("1. Total billionaires in " + selected_industry)
    st.table(billionaires_counts)

    st.title('2. Billionaires by Industry')
    billionaires_by_category = df.groupby('industries')['Billionaires'].count().reset_index()
    fig = px.line(billionaires_by_category, x="industries", y="Billionaires", title='Billionaires by Industry', height=500, width=700)
    fig.update_traces(line=dict(color='yellow'))
    st.plotly_chart(fig)



if x == 'Industry Wise Analysis':

    industry_list = df['industries'].unique().tolist()
    industry_list.insert(0, 'Overall')

    selected_industry = st.selectbox("Select an Industry ", industry_list)
    billionaires_counts = helper.industrywise_billionaires(df, selected_industry)
    if selected_industry == 'Overall':
        st.title("1. Overall Billionaires in each Industry")
    if selected_industry != 'Overall':
        st.title("1. Total billionaires in " + selected_industry)
    st.table(billionaires_counts)

    st.title("2. Distribution of Billionares (Bar Plot)")
    industry_df = df['industries'].value_counts().reset_index()
    industry_df.columns = ['industry', 'Billionaires']
    fig = px.bar(industry_df, x='industry', y='Billionaires', title='Number of Billionaires in Each Industry',
                 color='industry',
                 labels={'industry': 'Industry', 'Billionaires': 'Number of Billionaires'}, height=500, width=800)
    st.plotly_chart(fig)

    st.title("3. Distribution of Billionares (Pie chart)")
    industry_df = df['industries'].value_counts().reset_index()
    industry_df.columns = ['industry', 'Billionaires']
    fig = px.pie(industry_df, names='industry', values='Billionaires', title='Distribution of Billionaires by Industry',
                 height=700)
    st.plotly_chart(fig)

    st.title('4. Age VS Billionaires')
    famous_industries = ['Fashion & Retail', 'Automotive', 'Technology',
                         'Finance & Investments', 'Media & Entertainment', 'Telecom',
                         'Diversified', 'Food & Beverage', 'Logistics',
                         'Gambling & Casinos', 'Manufacturing', 'Real Estate',
                         'Metals & Mining', 'Energy', 'Healthcare', 'Service',
                         'Construction & Engineering', 'Sports']
    AGE = []
    industry = []
    for industry_name in famous_industries:
        temp_df = df[df['industries'] == industry_name]
        age_data = temp_df['age'].dropna()
        if not age_data.empty:
            AGE.append(age_data)
            industry.append(industry_name)

    fig = ff.create_distplot(AGE, industry, show_hist=False, show_rug=False)
    fig.update_layout(title_text='Age VS Billionaires in Each Industry')
    st.plotly_chart(fig)

    st.title('5. AgeGroup vs Billionaires')
    df['AgeGroup'] = pd.cut(df['age'], bins=[0, 30, 40, 50, 60, 70, 80, 90],
                            labels=['<30', '30-40', '40-50', '50-60', '60-70', '70-80', '80+'])
    billionaires_by_age = df.groupby(['industries', 'AgeGroup'])['Billionaires'].count().reset_index()
    color_map = {'<30': 'blue', '30-40': 'green', '40-50': 'purple', '50-60': 'orange', '60-70': 'red','70-80': 'magenta', '80+': 'cyan'}
    fig = px.line(billionaires_by_age, x="industries", y="Billionaires", title='AgeGroup vs Billionaires in Each Industry', color="AgeGroup", height=500, width=750, color_discrete_map=color_map)
    st.plotly_chart(fig)


    st.title('6. Billionaires by Industry')
    billionaires_by_category = df.groupby('industries')['Billionaires'].count().reset_index()
    fig = px.line(billionaires_by_category, x="industries", y="Billionaires", title='Billionaires by Industry', height=500, width=700)
    fig.update_traces(line=dict(color='yellow'))
    st.plotly_chart(fig)

if x == 'Country wise Billionaires':
    country_list = df['country'].unique().tolist()
    country_list.insert(0, 'Overall')

    selected_country = st.selectbox("Select a country ", country_list)
    billionaires_counts = helper.top_billionaires_by_country(df, selected_country)
    st.title(selected_country + " Top billionaires" )
    st.table(billionaires_counts)








