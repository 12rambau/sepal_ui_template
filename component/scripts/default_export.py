from pathlib import Path

import ee
from sepal_ui.scripts import gee
from sepal_ui.scripts.run_aoi_selection import isAsset

ee.Initialize()

def export_dataset(aoi_io, scale, dataset):
    """export the given dataset as an asset using the provided scale cliped on the aoi_io"""
    
    # create a filename out of the aoi name 
    filename = f"template_hansen_export_{aoi_io.get_aoi_name()}"
    
    # get the root folder of the user 
    folder = Path(ee.data.getAssetRoots()[0]['id'])
    asset_name = folder/filename
    
    # check if the asset already exist
    if isAsset(str(asset_name), str(folder)):
        raise Exception(cm.default_gee.asset_exist.format(asset_name))
        return asset_name
    
    # launch the export
    task_config = {
        'image': dataset,
        'description': filename,
        'assetId': str(asset_name),
        'scale': int(scale), 
        'region': aoi_io.get_aoi_ee().geometry(),
        'maxPixels': 1e13
    }
    
    task = ee.batch.Export.image.toAsset(**task_config)
    task.start()
    
    return asset_name