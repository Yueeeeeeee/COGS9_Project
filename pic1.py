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

data_pic1 = pd.read_excel('rate.xlsx').values
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

data = pd.read_csv('master.csv')
data = data[data['year'] < 2015]
df0 = data[['year', 'suicides_no']]
df0 = df0.groupby(['year'], as_index=False).agg({'suicides_no': 'sum'})
df1 = data[['year', 'sex', 'suicides_no']]
df1 = df1.groupby(['year', 'sex'], as_index=False).agg({'suicides_no': 'sum'})

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

title = 'Total Suicides vs. Year'
labels = ['Total', 'Male', 'Female']
colors = ['rgb(115,115,115)', 'rgb(49,130,189)',
          'rgb(189,189,189)']  # rgb(67,67,67)'

mode_size = [12, 8, 8]
line_size = [4, 2, 2]

x_data = np.array([df0['year'], df0['year'], df0['year']])

y_data = np.array([df0['suicides_no'].values, df1[df1['sex'] == 'male']
                   ['suicides_no'].values, df1[df1['sex'] == 'female']['suicides_no'].values])

fig1 = go.Figure()

for i in range(0, 3):
    fig1.add_trace(go.Scatter(x=x_data[i], y=y_data[i], mode='lines', name=labels[i], line=dict(
        color=colors[i], width=line_size[i])))

    # endpoints
    fig1.add_trace(go.Scatter(x=[x_data[i][0], x_data[i][-1]], y=[y_data[i][0], y_data[i]
                                                                  [-1]], mode='markers', marker=dict(color=colors[i], size=mode_size[i])))

fig1.update_layout(
    xaxis=dict(
        showline=True,
        showgrid=False,
        showticklabels=True,
        linecolor='rgb(204, 204, 204)',
        linewidth=2,
        ticks='outside',
        tickfont=dict(
            family='Arial',
            size=12,
            color='rgb(82, 82, 82)',
        ),
    ),
    yaxis=dict(
        showgrid=False,
        zeroline=False,
        showline=False,
        showticklabels=False,
    ),
    autosize=True,
    margin=dict(
        autoexpand=False,
        l=100,
        r=20,
        t=110,
    ),
    showlegend=False,
    plot_bgcolor='white'
)

annotations = []

# Adding labels
for y_trace, label, color in zip(y_data, labels, colors):
    # labeling the left_side of the plot
    annotations.append(dict(xref='paper', x=0.05, y=y_trace[0], xanchor='right', yanchor='middle',
                            text=label + ' {}'.format(y_trace[0]), font=dict(family='Arial', size=16), showarrow=False))
    # labeling the right_side of the plot
    annotations.append(dict(xref='paper', x=0.95, y=y_trace[11], xanchor='left', yanchor='middle',
                            text='{}'.format(y_trace[11]), font=dict(family='Arial', size=16), showarrow=False))

annotations.append(dict(x=0.5, y=0.2, xref='paper', yref='paper',
                        text='Source: <a href="https://www.kaggle.com/russellyates88/suicide-rates-overview-1985-to-2016"> Kaggle</a>',
                        showarrow=False))

fig1.update_layout(title_text='Total Suicides vs. Year',
                   geo=dict(
                       showframe=False,
                       showcoastlines=False,
                       projection_type='equirectangular'
                   ), annotations=annotations)

fig1.show()
