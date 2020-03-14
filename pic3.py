import numpy as np
import pandas as pd
import pycountry
import plotly.express as px
import plotly.graph_objects as go
from collections import defaultdict


""" source = px.data.gapminder()
source = source.groupby(['country','iso_alpha'],as_index=False).agg({'iso_num': 'mean'})
country_code = defaultdict(str)
for i in source.iterrows():
    country_code[i[1][0]] = i[1][1]
    
country_code['Antigua and Barbuda'] = 'ATG'
country_code['Bahamas'] = 'BHS'
country_code['Barbados'] = 'BRB'
country_code['Belize'] = 'BLZ'
country_code['Luxembourg'] = 'LUX'
country_code['Malta'] = 'MLT'
country_code['Republic of Korea'] = 'KOR'
country_code['Saint Lucia'] = 'LCA'
country_code['Saint Vincent and Grenadines'] = 'VCT'
country_code['Seychelles'] = 'SYC'
country_code['Suriname'] = 'SUR'
country_code['Turkmenistan'] = 'TKM'
country_code['Ukraine'] = 'UKR' """

countries = defaultdict(str)
for country in pycountry.countries:
    countries[country.name] = country.alpha_3

countries['Russia'] = 'RUS'
countries['Ivory Coast'] = 'CIV'
countries['South Korea'] = 'KOR'
countries['Cape Verde'] = 'CPV'
countries['Moldova'] = 'MDA'
countries['Bolivia'] = 'BOL'
countries['F.S. Micronesia'] = 'FSM'
countries['North Korea'] = 'PRK'
countries['Slovak Republic'] = 'SVK'
countries['Czech Republic'] = 'CZE'
countries['Tanzania'] = 'TZA'
countries['Laos'] = 'LAO'
countries['Vietnam'] = 'VNM'
countries['East Timor'] = 'TMP'
countries['Brunei'] = 'BRU'
countries['Iran'] = 'IRN'
countries['Venezuela'] = 'VEN'
countries['São Tomé and Príncipe'] = 'STP'
countries['Syria'] = 'SYR'
countries['DR Congo'] = 'COD'

OECD = ['MEX', 'KOR', 'GRC', 'IND', 'CHL', 'RUS', 'POL', 'LVA', 'ISR', 'ISL', 'IRL', 'EST', 'PRT', 'USA', 'CZE', 'HUN', 'NZL', 'SVK',
        'ITA', 'JPN', 'CAN', 'ESP', 'SVN', 'GBR', 'AUS', 'FIN', 'SWE', 'AUT', 'CHE', 'BEL', 'LUX', 'FRA', 'NLD', 'NOR', 'DNK', 'DEU']

data_pic1 = pd.read_excel('data1.xlsx').values
data1 = []
data2 = []

for i in data_pic1[:, 1]:
    if i.endswith('[a]\xa0(more info)'):
        data1.append(i[:-15].strip())
    elif i.endswith('(more info)'):
        data1.append(i[:-12].strip())
    elif i.endswith('[a]'):
        data1.append(i[:-3].strip())
    else:
        data1.append(i.strip())

for i in data1:
    data2.append(countries[i])

data_pic1[:, 1] = data1
data_pic1[:, 2] = data2

data_pic1 = pd.DataFrame(data=data_pic1, columns=[
                         'Rank', 'Country', 'Code', 'Rate'])

data_pic2 = pd.read_excel('data2.xlsx').values
data1 = []
data2 = []
data3 = []

for i in data_pic2[:, 1]:
    data1.append(i.strip())

for i in data1:
    data2.append(countries[i])

for i in data2:
    data3.append(data_pic1[data_pic1['Code'] == i]['Rate'].values[0])

data_pic2[:, 1] = data1
data_pic2[:, 2] = data2
data_pic2[:, 4] = data3

data_pic2 = pd.DataFrame(data=data_pic2, columns=[
                         'Rank', 'Country', 'Code', 'Hours', 'Rate'])

data_pic3 = pd.read_excel('data3.xlsx').values
unemployment = defaultdict(float)
for i in range(len(data_pic3)):
    unemployment[countries[data_pic3[i, 1].strip()]] = data_pic3[i, 2]

data4 = []
for i in data_pic2['Code']:
    data4.append(unemployment[i])

try:
    data_pic2.insert(5, 'Unemployment', data4)
except:
    print('Insert done before!')

data_pic4 = pd.read_excel('data4.xlsx').values
gdp_ppp = defaultdict(float)
for i in range(len(data_pic4)):
    gdp_ppp[countries[data_pic4[i, 1].strip()]] = data_pic4[i, 2]

data5 = []
for i in data_pic2['Code']:
    data5.append(gdp_ppp[i])

try:
    data_pic2.insert(6, 'GDP', data5)
except:
    print('Insert done before!')

data_pic5 = pd.read_excel('data5.xlsx').values
welfare = defaultdict(float)
for i in range(len(data_pic5)):
    welfare[countries[data_pic5[i, 1].strip()]] = data_pic5[i, 2]

data5 = []
for i in data_pic2['Code']:
    data5.append(welfare[i])

try:
    data_pic2.insert(7, 'Welfare', data5)
except:
    print('Insert done before!')

fig1 = go.Figure(data=go.Choropleth(
    locations=data_pic2['Code'],
    z=data_pic2['Rate'],
    text=data_pic2['Country'],
    colorscale='Blues',
    autocolorscale=False,
    reversescale=False,
    marker_line_color='darkgray',
    marker_line_width=0.5,
    colorbar_title='Suicide Rate',
))

fig1.update_layout(
    title_text='Suicides in 100k Population',
    geo=dict(
        showframe=False,
        showcoastlines=False,
        projection_type='equirectangular'
    ),
    annotations=[dict(
        x=0.5,
        y=0.2,
        xref='paper',
        yref='paper',
        text='Source: <a href="https://en.wikipedia.org/wiki/List_of_countries_by_suicide_rate">\
            Wikipedia</a>',
        showarrow=False
    )]
)

fig1.show()

fig2 = go.Figure(data=go.Choropleth(
    locations=data_pic2['Code'],
    z=data_pic2['GDP'],
    text=data_pic2['Country'],
    colorscale='Blues',
    autocolorscale=False,
    reversescale=False,
    marker_line_color='darkgray',
    marker_line_width=0.5,
    colorbar_title='GDP in $',
))

fig2.update_layout(
    title_text='GDP per Capital (PPP)',
    geo=dict(
        showframe=False,
        showcoastlines=False,
        projection_type='equirectangular'
    ),
    annotations=[dict(
        x=0.5,
        y=0.2,
        xref='paper',
        yref='paper',
        text='Source: <a href="https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(PPP)_per_capita">\
            Wikipedia</a>',
        showarrow=False
    )]
)

fig2.show()

fig3 = go.Figure(data=go.Choropleth(
    locations=data_pic2['Code'],
    z=data_pic2['Welfare'],
    text=data_pic2['Country'],
    colorscale='Blues',
    autocolorscale=False,
    reversescale=False,
    marker_line_color='darkgray',
    marker_line_width=0.5,
    colorbar_title='Social Welfare / GDP',
))

fig3.update_layout(
    title_text='Social Welfare as Percentage of GDP',
    geo=dict(
        showframe=False,
        showcoastlines=False,
        projection_type='equirectangular'
    ),
    annotations=[dict(
        x=0.5,
        y=0.2,
        xref='paper',
        yref='paper',
        text='Source: <a href="https://en.wikipedia.org/wiki/List_of_countries_by_social_welfare_spending">\
            Wikipedia</a>',
        showarrow=False
    )]
)

fig3.show()
