import os
from pathlib import Path

from sepal_ui.translator import Translator

# the sepal_ui allows you to create a translation interface
# it's a good practice to build your app translatio-ready
# The translator object is using the value defined in the paramter file of your SEPAL instance
# to guess the language to use

# create a ms object that will be used to translate all the messages
# the base language is english and every untranslated messages will be fallback to the english key
# complete the json file the add keys in the app
# avoid hard written messages at all cost
cm = Translator(Path(__file__).parent)
