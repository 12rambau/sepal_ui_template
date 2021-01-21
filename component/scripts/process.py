import time
import sys
import os
from pathlib import Path

import numpy as np
import pandas as pd
import geemap
import ee
import ipyvuetify as v
from matplotlib import pyplot as plt
from ipywidgets import Output

from sepal_ui.mapping import SepalMap

from ..message import ms

ee.Initialize()

def run_my_process(output, pcnt, name):
    
    # error example on one variable 
    # catch errors allows you to display specific messages to your user in the output widget with the error coloring
    if pcnt < 50: 
        raise Exception(f'{pcnt} is not big enough')
    
    # the file will be written in the tmp directory 
    # prefer the use of the Path object than the os.path strings as specify in PEP 8 convention
    pathname = Path('~', 'tmp', f'fake_csv_{name}_{pcnt}.csv').expanduser()
    
    # create a fake dataframe and save it in tmp
    df = pd.DataFrame(np.random.randint(0, pcnt, size=(pcnt, 4)), columns=list('ABCD'))
    df.to_csv(pathname, index=False)
    
    # fake the loading of something so that the user see the btn spining
    time.sleep(3)
    
    # let the user know that you managed to do something
    output.add_live_msg('Computation complete', 'success')
    
    return pathname

def create_fake_result(ee_aoi):
    
    # generate some fake data
    np.random.seed(0)
    n = 2000
    x = np.linspace(0.0, 10.0, n)
    y = np.cumsum(np.random.randn(n)*10).astype(int)
    
    # create a pyplot figure
    # to be displayed, the figure need to be written in an Output widget 
    fig_hist = Output()
    with fig_hist:
        # be aware that the sepal_ui color use dark theme so we'll use the matplotlib dark theme as well 
        with plt.style.context('dark_background'):
            fig, ax = plt.subplots(figsize=(20,10))
            ax.hist(y, bins=25, color=[v.theme.themes.dark.primary], histtype='bar', stacked=True, edgecolor='black', rwidth=0.8)
            ax.set_title('Histogram', fontweight="bold")
            
            plt.show()
    
    # set up a map with 
    m = SepalMap(['CartoDB.DarkMatter']) # you can choose in all the available basemaps of leaflet 
    m.zoom_ee_object(ee_aoi.geometry())
    
    # add the object borders in blue 
    empty = ee.Image().byte()
    outline = empty.paint(featureCollection = ee_aoi, color = 1, width = 3)
    # if you want to use a more javascript like use of the google api, use the **{} to set your function parameters
    # outline = empty.paint(**{'featureCollection': aoi_ee, 'color': 1, 'width': 3})
    m.addLayer(outline, {'palette': v.theme.themes.dark.info}, 'aoi') # I decided to use a color from the template
    m.zoom_ee_object(ee_aoi.geometry())
    
    
    # here I will only clip and display a the result of this tutorial : https://developers.google.com/earth-engine/tutorials/tutorial_forest_02
    # you can do whatever GEE process to produce you image before displaying it  
    dataset = ee.Image('UMD/hansen/global_forest_change_2015').clip(ee_aoi)
    m.addLayer(dataset, {'bands': 'treecover2000'}, 'treecover2000') # printing the forest coverage in 2000
    m.addLayer(dataset, {'bands': ['last_b50', 'last_b40', 'last_b30']}, 'healthy vegetation') # mapping the forest in 2015
    m.addLayer(dataset, {'bands': ['loss', 'treecover2000', 'gain']}, 'green') # map the gain and losses 
    m.addLayer(dataset, {'bands': ['loss', 'treecover2000', 'gain'], max: [1,255,1]}, 'green update') # map the gain and losses with bright colors

    GainAndLoss = dataset.select('gain').And(dataset.select('loss'));
    m.addLayer(GainAndLoss.updateMask(GainAndLoss), { 'palette': 'FF00FF'}, 'gain & loss') # map the place where gain and loss happened
    
    return fig_hist, m
    
    
    