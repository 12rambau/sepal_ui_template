import time
import sys
from sepal_ui.scripts import utils
import numpy as np
import pandas as pd
import os
import shutil
from bqplot import pyplot as plt 
import geemap
import ee

ee.Initialize()



def run_my_process(output, percentage, name):
    
    #variable check                      
    if percentage == None or percentage < 50:
        utils.displayIO(output, '{} is not big enough'.format(str(percentage)), alert_type='error')
        return 
    if name == None:
        utils.displayIO(output, 'Name has not been set', alert_type='error')
        return
    
    #empty the tmp directory
    tmpDir = os.path.dirname(os.path.abspath(__file__)) + '/../tmp/'
    if os.path.isdir(tmpDir):
        shutil.rmtree(tmpDir)
    
    #create the directory 
    os.mkdir(tmpDir)
    pathname = tmpDir + name + '.csv'
    
    #create a fake dataframe and save it in tmp
    df = pd.DataFrame(np.random.randint(0,percentage,size=(percentage, 4)), columns=list('ABCD'))
    df.to_csv(pathname, index=False)
    
    #wait for the loading button 
    time.sleep(3)
    
    utils.displayIO(output, 'Computation complete', alert_type='success')
    
    return pathname

def create_fake_result(asset='users/bornToBeAlive/aoi_AG'):
    
    # generate some fake data
    np.random.seed(0)
    n = 2000
    x = np.linspace(0.0, 10.0, n)
    y = np.cumsum(np.random.randn(n)*10).astype(int)
    
    # create a bqplot figure
    fig_hist = plt.figure(title='Histogram')
    hist = plt.hist(y, bins=25)
    fig_hist
    
    #set up a map with country boundaries
    center = [0, 0]
    zoom = 2
    
    m = geemap.Map(center=center, zoom=zoom)
    m.clear_layers()
    m.clear_controls()
    m.add_basemap('SATELLITE')
    m.add_control(geemap.ZoomControl(position='topright'))
    m.add_control(geemap.LayersControl(position='topright'))
    m.add_control(geemap.AttributionControl(position='bottomleft'))
    m.add_control(geemap.ScaleControl(position='bottomleft', imperial=False))
    
    country = ee.FeatureCollection(asset)
    m.addLayer(country, {}, 'country')
    m.centerObject(country, 5)
    
    return fig_hist, m
    
    
    