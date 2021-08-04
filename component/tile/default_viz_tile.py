# It is strongly suggested to use a separate file to define the tiles of your process and then call them in your notebooks. 
# it will help you to have control over their fonctionalities using object oriented programming

from sepal_ui import sepalwidgets as sw
from sepal_ui.scripts.utils import loading_button
import ipyvuetify as v

from component import scripts
from component.message import cm

# the tiles should all be heriting from the sepal_ui Tile object 
# if you want to create extra reusable object, you can define them in an extra widget.py file 
class DefaultVizTile(sw.Tile):
    
    def __init__(self, model, aoi_model, result_tile, **kwargs):
        
        # define the model and the aoi_model as class attribute so that they can be manipulated in its custom methods
        self.model = model
        self.aoi_model = aoi_model
        
        # as I will display my results in another tile, I need to gather this extra tile in my attributes
        self.result_tile = result_tile
        
        # create all the widgets that you want to use in the tile
        # create the widgets following ipyvuetify lib requirements (more information in the ipyvuetify and sepal_ui doc)
        # if you want to use them in custom function you should consider adding them in the class attirbute
        self.slider = v.Slider(
            label       = cm.default_process.slider, 
            class_      = "mt-5", 
            thumb_label = True, 
            v_model     = 0
        )
        
        self.text = v.TextField(
            label   = cm.default_process.textfield, 
            v_model = None
        )
        
        # link the widgets to the model 
        model \
            .bind(self.slider, 'slider_value') \
            .bind(self.text, 'text_value')
        
        # construct the Tile with the widget we have initialized 
        super().__init__(
            id_    = "default_viz_tile", # the id will be used to make the Tile appear and disapear
            title  = cm.default_process.title, # the Title will be displayed on the top of the tile
            inputs = [self.slider, self.text],
            btn    = sw.Btn(),
            alert  = sw.Alert()
        )
        
        # now that the Tile is created we can link it to a specific function
        self.btn.on_event('click', self._on_run)
        
    # in the pep 8 convention, "_" in the beggining of a method name
    # specify that the function is not supposed to be called outside the class (same as private declaration in C/C++)
    # the 3 parameters (widget, data, event)are the mandatory paramater of the javascript callback, we will only use widget
    # the decorator will be helpfull for debuging. your fonction is wrapped in a try except loop. 
    @loading_button(debug=False)
    def _on_run(self, widget, data, event): 
            
        # check that the input that you're gonna use are set 
        # this step is not mandatory but helps catching error 
        if not self.alert.check_input(self.aoi_model.name): raise Exception(cm.default_process.no_aoi)
        if not self.alert.check_input(self.model.slider_value): raise Exception(cm.default_process.no_slider)
        if not self.alert.check_input(self.model.text_value): raise Exception(cm.default_process.no_textfield)
            
        # launch any process you want, here it's defined in the scripts file
        csv_path = scripts.default_csv(
            output = self.alert, 
            pcnt   = self.model.slider_value, 
            name   = self.model.text_value
        )
        self.result_tile.down_btn.set_url(str(csv_path))
        
        # create a fake pyplot
        scripts.default_hist(self.result_tile.fig)
        
        # create maps
        dataset = scripts.default_maps(self.aoi_model.feature_collection, self.result_tile.m)
            
        # change the model values as its a mutable object 
        # useful if the model is used as an input in another tile
        self.model.csv_path = csv_path
        self.model.dataset = dataset
            
        # conclude the computation with a message
        self.alert.add_live_msg(cm.default_process.end_computation, 'success')
        
        return
        
        