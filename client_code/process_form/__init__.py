from ._anvil_designer import process_formTemplate
from anvil import *


class process_form(process_formTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('setup_form')

  def process_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('process_form')
