# It is strongly suggested to use a separate file to define the tiles of your process and then call them in your notebooks. 
# it will help you to have control over their fonctionalities using object oriented programming

from sepal_ui import sepalwidgets as sw
import ipyvuetify as v

from ..message import ms

# create an empty result tile that will be filled with displayable plot, map, links, text
class ResultTile(sw.Tile):
    
    def __init__(self, **kwargs):
        
        # note that btn and output are not a madatory attributes 
        super().__init__(
            id_ = "result_widget",
            title = ms.result.title,
            inputs = [ms.result.no_result]
        )