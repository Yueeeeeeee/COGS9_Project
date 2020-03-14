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
countries['Czech Republic'] = 'CSE'
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

data = pd.read_excel('data1.xlsx').values
data1 = []
data2 = []
for i in data[:, 1]:
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

data[:, 1] = data1
data[:, 2] = data2

data = pd.DataFrame(data=data, columns=['Rank', 'Country', 'Code', 'Rate'])
fig = go.Figure(data=go.Choropleth(
    locations=data['Code'],
    z=data['Rate'],
    text=data['Country'],
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

fig.show()
