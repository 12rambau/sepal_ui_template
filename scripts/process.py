import time
import sys
import numpy as np
import pandas as pd
import os
import shutil
from bqplot import pyplot as plt 
import geemap
import ee
from sepal_ui.mapping import SepalMap

ee.Initialize()



def run_my_process(output, percentage, name):
    
    #variable check                      
    if percentage == None or percentage < 50:
        output.add_live_msg('{} is not big enough'.format(str(percentage)), 'error')
        return 
    if name == None:
        output.add_live_msg('Name has not been set', 'error')
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
    
    output.add_live_msg('Computation complete', 'success')
    
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
    
    m = SepalMap(['SATELLITE'])    
    country = ee.FeatureCollection(asset)
    m.addLayer(country, {}, 'country')
    m.zoom_ee_object(country.geometry())
    
    return fig_hist, m
    
    
    