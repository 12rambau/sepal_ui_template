# It is strongly suggested to use a separate file to define the tiles of your process and then call them in your notebooks. 
# it will help you to have control over their fonctionalities using object oriented programming

from sepal_ui import sepalwidgets as sw
import ipyvuetify as v

from component import scripts as cs
from component.message import cm
from component import widget as cw

# the tiles should all be heriting from the sepal_ui Tile object 
# if you want to create extra reusable object, you can define them in an extra widget.py file 
class DefaultExportTile(sw.Tile):
    
    def __init__(self, io, aoi_io, **kwargs):
        
        # define the io and the aoi_io as class attribute so that they can be manipulated in its custom methods
        self.io = io 
        self.aoi_io = aoi_io
        
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
            output = sw.Alert()
        )
        
        # now that the Tile is created we can link it to a specific function
        self.btn.on_event('click', self._export_to_asset)
        
    # in the pep 8 convention, "_" in the beggining of a method name
    # specify that the function is not supposed to be called outside the class (same as private declaration in C/C++)
    # the 3 parameters (widget, data, event)are the mandatory paramater of the javascript callback, we will only use widget
    def _export_to_asset(self, widget, event, data): 
            
        # toggle the loading buttons
        # toogling the btns will insure that the user don't launch the process multiple times
        self.btn.toggle_loading()
            
        # check that the input that you're gonna use are set 
        # this step is not mandatory but helps catching error 
        if not self.output.check_input(self.io.dataset, cm.default_process.no_dataset): return self.btn.toggle_loading()
            
        # You don't want the end user to be stuck if an error occured 
        # it's a good habit to wrap the process in a try catch statement 
        # the error will be dispayed in the output so that a developer can work on the problem 
        # for debugging purpose, you need to silence this block to access the full traceback
        try:
            
            asset_name = cs.export_dataset(self.aoi_io, self.scale.v_model, self.io.dataset)
            
            # conclude the computation with a message
            self.output.add_live_msg(cm.default_gee.task_launched.format(asset_name), 'success')
            
        except Exception as e: 
            self.output.add_live_msg(str(e), 'error')
        
        # release the btns
        self.btn.toggle_loading()
        
        return