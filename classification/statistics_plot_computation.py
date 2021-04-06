#!/usr/bin/env python
# coding: utf-8

# In[117]:


get_ipython().system(' python -m spacy download pt_core_news_sm')


# In[30]:


# imports

import pandas as pd

from shapely.geometry import shape, Point, Polygon
import pandas as pd
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
import json
import plotly.express as px
import plotly
from utils import colors
from utils import font_for_plots


# # Read Data

# In[79]:


# read data
df = pd.read_csv('./data/classified_news.tsv', sep='\t')

# crimes per year
df['arquivo_date'] = pd.to_datetime(df.arquivo_date, errors='coerce')
df_crimes = df[df['feminicidio_case'] == 1]


# In[80]:


#df_crimes = df_crimes.iloc[::-1]
#df_crimes = df_crimes.head(10)
df_crimes.shape


# # 1 Data Geo annotation

# In[81]:


# News per location
# we will use geo locator to help us getting the country and region
import spacy
from geopy.geocoders import Nominatim
import time


# In[82]:


nlp = spacy.load('pt_core_news_lg')
geolocator = Nominatim(user_agent="dictionary_experiment")

# we define a minimum quality for the result from the geolocator
geo_quality_threshold = 0.55

# we define new dataframe columns with values to replace late
df_crimes['country'] = 'missing'
df_crimes['region'] = 'missing'
df_crimes['lat'] = 999
df_crimes['lon'] = 999
country_list = []
region_list = []
lat_list = []
lon_list = []


# for every row we try to compute those values
for iter, row in df_crimes.iterrows():

    # help debug
    print('')
    print(row['news_site_title'])

    # this will extract entities from spacy
    doc = nlp(row['news_site_text'] + ' ' + row['news_site_title'])

    # define storage variables
    locals_name = []
    locals_country = []
    locals_region = []
    locals_lat = []
    locals_lon = []

    # for every identified entity
    for entity in doc.ents:
        # we only want location entities
        if entity.label_ == 'LOC':
            # for debug
            #print(entity.label_)
            #print(entity.text)
            # we try to locate the entity
            try:
                lc = geolocator.geocode(entity.text, timeout=10)
                time.sleep(2)

                # sometimes the geo object returned is none
                if lc is not None:
                    geo_evaluation = lc.raw['importance']

                    # when the result has a certain quality
                    if geo_evaluation > geo_quality_threshold:
                        #print(lc.raw)
                        # we get the desired variables
                        type_org = lc.raw['type']
                        lat = lc.raw['lat']
                        lon = lc.raw['lon']
                        relc = geolocator.reverse([lc.latitude, lc.longitude], language='en')
                        #print(relc.raw['address'])
                        country = relc.raw['address']['country']

                        # if country is portugal we want to know the district, we dont ask for all because the json names vary according to country
                        if country == 'Portugal':
                            try:
                                region = relc.raw['address']['state_district']
                            except:
                                try:
                                    region = relc.raw['address']['state']
                                except:
                                    region = 'unknown'
                        else:
                            region = 'unknown'

                        # we store the found values
                        locals_name.append(entity.text)
                        locals_country.append(country)
                        locals_region.append(region)
                        locals_lat.append(lat)
                        locals_lon.append(lon)

            except Exception as e:
                print('')
                print('error')
                print(e)

    # helps debug
    #print(locals_name)
    #print(locals_country)
    #print(locals_region)
    #print(locals_lat)
    #print(locals_lon)

    country = 'unknown'
    region = 'unknown'
    lat = 999
    lon = 999
    # choose the country that is the majority and add this to the country column
    percentage_portugal = 0
    # prevents division by 0
    if len(locals_country) > 0:
        percentage_portugal = locals_country.count('Portugal') / len(locals_country)
        if percentage_portugal >= 0.5:
            country = 'Portugal'
        else:
            country = max(set(locals_country), key=locals_country.count)

        # make the average of latitude and longitude, because they are very close so we can just average
        msk = [el == country for el in
               locals_country]  # mask to select in a list the elements that are for the desired country
        locals_lat = [locals_lat[i] for i in range(len(locals_lat)) if msk[i]]
        locals_lon = [locals_lon[i] for i in range(len(locals_lon)) if msk[i]]
        locals_lat = list(map(float, locals_lat))
        locals_lon = list(map(float, locals_lon))
        lat = sum(locals_lat) / len(locals_lat)
        lon = sum(locals_lon) / len(locals_lon)

        # and ask to the api again to which region does it correspond and add it to the dataframe
        try:
            relc = geolocator.reverse([lat, lon], language='en')
            time.sleep(2)
        except:
            region = 'unknown'

        try:
            region = relc.raw['address']['state_district']
        except:
            try:
                region = relc.raw['address']['state']
            except:
                region = 'unknown'

    print(country)
    print(region)
    print(lat)
    print(lon)

    # add values in the dataframe column
    #df_crimes['country'].iloc[iter] = country
    #df_crimes['region'].iloc[iter] = region
    #df_crimes['lat'].iloc[iter] = lat
    #df_crimes['lon'].iloc[iter] = lon
    country_list.append(country)
    region_list.append(region)
    lat_list.append(lat)
    lon_list.append(lon)

        


# In[83]:


print(len(country_list))
print(country_list)
print(len(region_list))
print(region_list)      
print(len(lat_list))
print(lat_list)
print(len(lon_list))
print(lon_list)


# In[85]:


df_crimes['country'] = country_list
df_crimes['region'] = region_list
df_crimes['lat'] = lat_list
df_crimes['lon'] = lon_list

df_crimes


# In[86]:


df_crimes.to_csv('./data/df_crimes_geo_location.tsv',sep='\t',index=False)


# # 2 - Select all data for Continental Portugal (exclude Azores and Madeira)

# In[88]:


# read geo maps
continental_states = gpd.read_file('./data/pt_continental.geojson')
azores_states = gpd.read_file('./data/pt_açores.geojson')
madeira_states = gpd.read_file('./data/pt_madeira.geojson')


# In[89]:


# read crimes and select portugal
df_crimes = pd.read_csv('./data/df_crimes_geo_location.tsv', sep='\t')
df_crimes_portugal = df_crimes[df_crimes['country'] == 'Portugal']


# In[90]:


# annotate with Geojson district
def point_which_portuguese_district(point):
  msk = continental_states.contains(point)
  if sum(msk) != 0:
    return [continental_states['Distrito'][i] for i in range(len(continental_states['Distrito'])) if msk[i]][0]
  msk = azores_states.contains(point)
  if sum(msk) != 0:
    return [azores_states['NUT1_DSG'][i] for i in range(len(azores_states['NUT1_DSG'])) if msk[i]][0]
  msk = madeira_states.contains(point)
  if sum(msk) != 0:
    return [madeira_states['Ilha'][i] for i in range(len(madeira_states['Ilha'])) if msk[i]][0]
  return 'none'

df_crimes_portugal['district'] = 'empty'
for iter, row in df_crimes_portugal.iterrows():
  district = point_which_portuguese_district(Point(row['lon'],row['lat']))
  df_crimes_portugal.at[iter,'district'] = district


# In[91]:


# Divide crimes per continental, madeira, azores
df_crimes_portugal.loc[:,'cont_mad_azo'] = 'unknown'
df_crimes_portugal.loc[df_crimes_portugal['district'].isin(continental_states['Distrito'].values),'cont_mad_azo'] = 'continental'
df_crimes_portugal.loc[df_crimes_portugal['district'].isin(azores_states['NUT1_DSG'].values),'cont_mad_azo'] = 'açores'
df_crimes_portugal.loc[df_crimes_portugal['district'].isin(madeira_states['Ilha'].values),'cont_mad_azo'] = 'madeira'


# In[92]:


# select crimes for Continental Portugal
df_crimes_continental = df_crimes_portugal[df_crimes_portugal['cont_mad_azo'] == 'continental']


# In[93]:


df_crimes_continental_save = df_crimes_continental[['news_site_title','district']]
df_crimes_continental_save.to_csv('./data/df_crimes_continental_save.tsv', sep='\t',index=False)


# In[95]:


print(df_crimes_continental_save)


# # 3) Plot crimes per year in continental Portugal

# ### 3.1 Bar plot

# In[96]:


# crimes per year
df_crimes_continental['arquivo_date'] = pd.to_datetime(df_crimes_continental.arquivo_date, errors='coerce')
df_crimes_continental['dateyear'] = df_crimes_continental['arquivo_date'].dt.year
res = pd.DataFrame(df_crimes_continental.groupby(['dateyear']).size())
res['year'] = res.index
res.columns = ['Total Crimes', 'Ano']
res.to_csv('./data/crimes_per_year.tsv',sep='\t',index=False)


# In[97]:


fig = px.bar(res, x="Ano", y="Total Crimes")

fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text'],
    font_family=font_for_plots
)

fig.update_traces(marker_color=colors['plot_bar'])
fig.update_yaxes(showgrid=False,title='Total de Notícias de Feminicídios')
fig.update_xaxes(title='Ano')

fig.write_json('./data_to_visualize/plot_feminicide_per_year.json')

fig = plotly.io.read_json('./data_to_visualize/plot_feminicide_per_year.json')
fig


# ### 3.2 Table

# In[98]:


df_crimes_continental_table = df_crimes_continental[['news_site_title','dateyear','district']]
df_crimes_continental_table['district'] = df_crimes_continental_table['district'].str.capitalize()
df_crimes_continental_table.to_csv('./data_to_visualize/table_news_year_district.tsv',sep='\t',index=False)


# In[99]:


dict_tables_per_year = dict()
for year in set(df_crimes_continental_table['dateyear']):
    table_year = df_crimes_continental_table[df_crimes_continental_table['dateyear'] == year]
    df_table = table_year[['news_site_title','district']].sort_values("district", ascending=True)
    df_table.columns = ['Notícia', 'Distrito']
    dict_tables_per_year[year] = df_table.to_dict('records')

with open('./data_to_visualize/dict_tables_news_per_year.json', 'w') as outfile:
    json.dump(dict_tables_per_year, outfile)
    


# #  4) Plot crimes per district in continental Portugal

# ### 4.1 Plot

# In[104]:


# counts per region
res = df_crimes_continental.groupby(['district']).size()
dict_crimes_district = dict(res)
for state in continental_states['Distrito']:
    if state not in dict_crimes_district:
        dict_crimes_district[state] = 0

df_total_crimes_district = pd.DataFrame(list(dict_crimes_district.items()))
df_total_crimes_district = df_total_crimes_district.rename(columns={0: "Distrito", 1: 'crimes'})
df_total_crimes_district.to_csv('./data/total_crimes_district.tsv', sep='\t')
print(df_total_crimes_district)


# We tried to plot in a map, however it was too inneficient to load in the dash due to using geojson. So we opt to convert it to bar plot.

# In[106]:


goal_size = 500


# In[103]:


import json
with open('./data/continental_portugal_region.json') as json_file:
    continental_states_plot = json.load(json_file)

# sample coordinates

dict_state = {
    "AVEIRO": "OK",
    "BEJA": "OK",
    "BRAGA": "OK",
    "BRAGANÇA": "OK",
    "CASTELO BRANCO": "OK",
    "COIMBRA": "OK",
    "ÉVORA": "OK",
    "FARO": "SMALL",
    "GUARDA": "SMALL",
    "LEIRIA": "SMALL",
    "LISBOA": "DIVISIONS",
    "PORTALEGRE": "OK",
    "PORTO": "OK",
    "SANTARÉM": "OK",
    "SETÚBAL": "SMALL",
    "VIANA DO CASTELO": "SMALL",
    "VILA REAL": "OK",
    "VISEU": "OK"
    }

def sample_any_list(list_to_sample):
    list_size = len(list_to_sample)
    goal_size = 200
    n = int(list_size/goal_size)
    if n == 0: n = 1
    return list_to_sample[0::n]

def sample_coordinates(old_coordinates, district_name):
    if dict_state[district_name] == 'OK':
        old_coordinates = [[sample_any_list(old_coordinates[0][0])]]
    
    return old_coordinates

for district in continental_states_plot['features']:
    print(district['properties']['district'])
    print(len(district['geometry']['coordinates'][0][0])) 
    district['geometry']['coordinates'] = sample_coordinates(district['geometry']['coordinates'],district['properties']['district'])
    

for district in continental_states_plot['features']:
    print(district['properties']['district'])
    print(len(district['geometry']['coordinates'][0][0])) 
 
    
with open('./data/test.txt', 'w') as outfile:
    json.dump(continental_states_plot, outfile)
    
    


# In[107]:


fig_plot = px.choropleth(
    df_total_crimes_district,
    locations="Distrito",
    geojson=continental_states_plot,
    featureidkey="properties.district",
    color='crimes',
    projection="mercator",
    hover_name="Distrito",
    color_continuous_scale=[colors['map_min_gradient_color'],colors['map_max_gradient_color']],)
fig_plot.update_geos(fitbounds = "locations", visible = False, resolution=50)
fig_plot.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
                       plot_bgcolor=colors['background'],
                       paper_bgcolor=colors['background'],
                       font_color=colors['text'],
                       dragmode=False,
                       geo=dict(bgcolor=colors['background']),
                       font_family=font_for_plots
                       )

fig_plot.write_json('./data_to_visualize/plot_feminicide_per_district.json')


# In[108]:


fig_plot = plotly.io.read_json('./data_to_visualize/plot_feminicide_per_district.json')

fig_plot.show()


# #### 4.1.1 In bar plot

# In[110]:


df_total_crimes_district = df_total_crimes_district.sort_values(by='crimes', ascending=False)

fig = px.bar(df_total_crimes_district, x="Distrito", y="crimes")

fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text'],
    font_family=font_for_plots
)

fig.update_traces(marker_color=colors['plot_bar'])
fig.update_yaxes(showgrid=False,title='Total de Notícias de Feminicídios')
fig.update_xaxes(title='Distrito')

fig.write_json('./data_to_visualize/plot_feminicide_per_district_bar.json')

fig = plotly.io.read_json('./data_to_visualize/plot_feminicide_per_district_bar.json')
fig


# ### 4.2 Table

# In[111]:


dict_tables_per_district = dict()
for district in set(df_crimes_continental_table['district']):
    table_district = df_crimes_continental_table[df_crimes_continental_table['district'] == district]
    df_table = table_district[['news_site_title','dateyear']].sort_values("dateyear", ascending=False)
    df_table.columns = ['Notícia', 'Ano']
    dict_tables_per_district[district.upper()] = df_table.to_dict('records')

with open('./data_to_visualize/dict_tables_news_per_district.json', 'w') as outfile:
    json.dump(dict_tables_per_district, outfile)


# # 5) Animation with dots per crime

# In[112]:


import pandas as pd
import geopandas
import matplotlib.pyplot as plt

df_crimes_portugal_continental = df_crimes_portugal[df_crimes_portugal['cont_mad_azo'] == 'continental']
df_crimes_portugal_madeira = df_crimes_portugal[df_crimes_portugal['cont_mad_azo'] == 'madeira']
df_crimes_portugal_azores = df_crimes_portugal[df_crimes_portugal['cont_mad_azo'] == 'azores']


crimes_location_continental = geopandas.GeoDataFrame(
    df_crimes_portugal_continental, geometry=geopandas.points_from_xy(df_crimes_portugal_continental.lon, df_crimes_portugal_continental.lat, crs="EPSG:4258"))

crimes_location_madeira = geopandas.GeoDataFrame(
    df_crimes_portugal_madeira, geometry=geopandas.points_from_xy(df_crimes_portugal_madeira.lon, df_crimes_portugal_madeira.lat, crs="EPSG:4258"))

crimes_location_azores = geopandas.GeoDataFrame(
    df_crimes_portugal_azores, geometry=geopandas.points_from_xy(df_crimes_portugal_azores.lon, df_crimes_portugal_azores.lat, crs="EPSG:4258"))


# In[113]:


import plotly.express as px
import geopandas as gpd

# sort dataframe in reverse order
crimes_location_continental = crimes_location_continental.sort_values(by='arquivo_date', ascending=True)
crimes_location_continental.to_csv('./data/crimes_location_continental_ordered.tsv',sep='\t')


fig_anim = px.scatter_geo(crimes_location_continental,
                     lat="lat",
                     lon="lon",
                     projection="mercator",
                     hover_name="news_site_title",
                     animation_frame="arquivo_date",
                     title="Hello",
                     color_discrete_sequence=[colors['title']],
                    )

fig_anim.update_geos(center=dict(lat=39.68, lon=-8.03),scope="europe",
    visible=True, resolution=50,showocean=True,oceancolor=colors['background'],landcolor=colors['plot_bar'],
    showcountries =True,countrycolor=colors['background'],projection_scale=15, #this is kind of like zoom
    )

sliders = [dict(
    currentvalue={"prefix": "Data: "}
)]

fig_anim.update_traces(marker=dict(color=colors['title']))
fig_anim.update_layout(sliders=sliders,
                        title=crimes_location_continental['news_site_title'].iloc[0],
                        margin={"r":0,"t":30,"l":0,"b":0},
                        plot_bgcolor=colors['background'],
                        paper_bgcolor=colors['background'],
                        font_color=colors['text'],
                        dragmode=False,
                        geo=dict(bgcolor=colors['background']),
                       title_x=0.5,
                       font_family=font_for_plots
                       )

fig_anim.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 1500


for button in fig_anim.layout.updatemenus[0].buttons:
    button['args'][1]['frame']['redraw'] = True

for k in range(0,crimes_location_continental.shape[0]):
    fig_anim.frames[k]['layout'].update(title_text=crimes_location_continental['news_site_title'].iloc[k])












# In[114]:


fig_anim.write_json('./data_to_visualize/plot_animation.json')
fig_anim.show()


# In[115]:



fig_anim = plotly.io.read_json('./data_to_visualize/plot_animation.json')

fig_anim.show()

