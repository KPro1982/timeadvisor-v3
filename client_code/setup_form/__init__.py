from ._anvil_designer import setup_formTemplate
from anvil import *
import anvil.server
import anvil.media
import json



class setup_form(setup_formTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # anvil.server.call('say_hello', 'Anvil Developer')

    # Any code you write here will run before the form opens.

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('setup_form')

  def process_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('process_form')

  def client_data_change(self, file, **event_args):
    print(file.name, file)
    anvil.server.call('SetClientData',file.name, file)


  def button_2_click(self, **event_args):
    text = anvil.server.call('ChangeName', 'clientdanny')
    self.return_text.text = text

  def json_path_change(self, file, **event_args):
    data = json.loads(self.json_path.file.get_bytes()) 
    self.json_display.text = data
    anvil.media.download(anvil.server.call('MakeXL', data))