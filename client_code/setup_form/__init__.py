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
    print("data type:", type(data))
    data = self.resize_list(data)
    newdata = []
    print("size: ", len(data))
    file = self.client_data.file

    for x in data:
      y = anvil.server.call('Process', x, file)  
      print("returned value: ", y)
      newdata.append(y)

      
    anvil.media.download(anvil.server.call('Save',newdata))
    
  def resize_list(self, big_list):
    new_list = []
    for x in big_list:
      try:
        print(x['subject'])
        new_list.append(x)
      except TypeError:
        return new_list
    return new_list