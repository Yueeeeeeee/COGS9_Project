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

fig = go.Figure(data=go.Choropleth(
    locations=data_pic1['Code'],
    z=data_pic1['Rate'],
    text=data_pic1['Country'],
    colorscale='Blues',
    autocolorscale=False,
    reversescale=False,
    marker_line_color='darkgray',
    marker_line_width=0.5,
    colorbar_title='Suicide Rate',
))

""" fig = go.Figure(data=go.Choropleth(
    locations=df1['iso_alpha'],
    z=df1['suicides/100k pop'],
    text=df1['country'],
    colorscale='Blues',
    autocolorscale=False,
    reversescale=False,
    marker_line_color='darkgray',
    marker_line_width=0.5,
    colorbar_title='Suicide Rate',
))

fig = px.choropleth(df1, locations="iso_alpha", color="suicides_no",
                    hover_name="country", color_continuous_scale=px.colors.sequential.Plasma) """

fig.update_layout(
    title_text='World Overview of Suicides in 100k Population by Country',
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

fig.show()
