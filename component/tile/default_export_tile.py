# It is strongly suggested to use a separate file to define the tiles of your process and then call them in your notebooks. 
# it will help you to have control over their fonctionalities using object oriented programming

from sepal_ui import sepalwidgets as sw
from sepal_ui.scripts.utils import loading_button
import ipyvuetify as v

from component import scripts as cs
from component.message import cm
from component import widget as cw

# the tiles should all be heriting from the sepal_ui Tile object 
# if you want to create extra reusable object, you can define them in an extra widget.py file 
class DefaultExportTile(sw.Tile):
    
    def __init__(self, model, aoi_model, **kwargs):
        
        # define the io and the aoi_io as class attribute so that they can be manipulated in its custom methods
        self.model = model
        self.aoi_model = aoi_model
        
        self.scale = cw.DefaultResInput(
            label = cm.default_process.scale,
            min_res = 10,
            max_res = 300
        )
        
        # construct the Tile with the widget we have initialized 
        super().__init__(
            id_    = "default_export_tile", # the id will be used to make the Tile appear and disapear
            title  = cm.default_process.export, # the Title will be displayed on the top of the tile
            inputs = [self.scale],
            btn    = sw.Btn(cm.default_process.export),
            alert  = sw.Alert()
        )
        
        # now that the Tile is created we can link it to a specific function
        self.btn.on_event('click', self._export_to_asset)
        
    # in the pep 8 convention, "_" in the beggining of a method name
    # specify that the function is not supposed to be called outside the class (same as private declaration in C/C++)
    # the 3 parameters (widget, data, event)are the mandatory paramater of the javascript callback, we will only use widget
    # the decorator will be helpfull for debuging. your fonction is wrapped in a try except loop. 
    @loading_button(debug=False)
    def _export_to_asset(self, widget, event, data): 
            
        # check that the input that you're gonna use are set 
        # this step is not mandatory but helps catching error 
        if not self.alert.check_input(self.model.dataset): raise Exception(cm.default_process.no_dataset)
            
        asset_name = cs.export_dataset(self.aoi_model, self.scale.v_model, self.model.dataset)
            
        # conclude the computation with a message
        self.alert.add_live_msg(cm.default_gee.task_launched.format(asset_name), 'success')
        
        return