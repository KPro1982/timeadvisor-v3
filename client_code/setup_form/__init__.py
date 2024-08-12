from ._anvil_designer import setup_formTemplate
from anvil import *
import anvil.server
import anvil.media
import json




class setup_form(setup_formTemplate):

  clientdata = False
  jsondata = False


  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.submit_button.enabled = False

    # Any code you write here will run before the form opens.

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('setup_form')

  def process_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('process_form')

  def client_data_change(self, file, **event_args):
    self.clientdata = True
    if(self.jsondata == True):
      self.submit_button.enabled = True
    

  def json_path_change(self, file, **event_args):
     self.jsondata = True
     if(self.clientdata == True):
       self.submit_button.enabled = True
    

  def submit_button_click(self, **event_args):
    data = json.loads(self.json_path.file.get_bytes())
    file = self.client_data.file
    anvil.media.download(anvil.server.call('Process',data,file))
    
