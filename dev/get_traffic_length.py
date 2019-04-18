

from natsort import natsorted
import geopandas as gpd
import pandas as pd

import os
import re

from datetime import datetime

times = []
traffic_length = []

root_dir = '../../data/Poster/traffic_data/'
figure_path = '../../data/Poster/traffic_figures/'

files = os.listdir('../../data/Poster/traffic_data/')

for file in natsorted(files):
    time = re.search('\d{2}:\d{2}', file).group(0)
    file_path = root_dir + file

    traffic = gpd.read_file(file_path)

    # convert
    traffic_sel = traffic[(traffic['fc'] < 5) & (traffic['jf'] > 4) & (traffic['cn'] > 0.5)]

    traffic_proj_sel_m = traffic_sel.to_crs({'init': 'epsg:32632'})
    print(time)
    traffic_length.append(int(traffic_proj_sel_m['geometry'].length.sum() / 1000))
    times.append(datetime.strptime(time, '%H:%M').time())



times_str = [time.strftime('%H:%M') for time in times]

df = pd.DataFrame(
    {'time':times_str,
     'traffic_length':traffic_length})

df.to_csv('../../data/Poster/traffic_figures/traffic_length2.csv')

import matplotlib.pyplot as plt
# test plot
df['new_index'] = list(range(1, 96))

df['new_index'] = df.date_range('2018-01-01', periods=3, freq='H')

df[]
df = df.set_index(df.index)

ax = df['traffic_length'].plot()
# ax.set_xticks(df.time)

ax.set_xticklabels(df.time, rotation=60)

cbar.get_ticklabels()[::2]

