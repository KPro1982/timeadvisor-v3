from ._anvil_designer import setup_formTemplate
from anvil import *
import anvil.server


class setup_form(setup_formTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    anvil.server.call('say_hello', 'Anvil Developer')

    # Any code you write here will run before the form opens.

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('setup_form')

  def process_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('process_form')

  def file_loader_1_change(self, file, **event_args):
    """This method is called when a new file is loaded into this FileLoader"""
    pass
