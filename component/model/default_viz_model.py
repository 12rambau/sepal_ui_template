from sepal_ui.model import Model
from traitlets import Any

# It is strongly suggested to us a separate file to define the io of your tile and process.
# it will help you to have control over it's fonctionality using object oriented programming

# in python variable are not mutable object (their value cannot be changed in a function)
# Thus use a class to define your input and output in order to have mutable variables
class DefaultVizModel(Model):

    # set up your inputs
    slider_value = Any(None).tag(sync=True)
    text_value = Any(None).tag(sync=True)

    # set up your output
    link = Any(None).tag(sync=True)
    dataset = Any(None).tag(sync=True)
