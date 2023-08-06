from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty, StringProperty

class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

class LoadDialog_MIC(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

class LoadDialog_API_INPUT(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

class SaveDialog(FloatLayout):
    save = ObjectProperty(None)
    text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)

class DataItem(object):
    def __init__(self, text='', is_selected=False):
        self.text = text
        self.is_selected = is_selected
        self.mark = False

