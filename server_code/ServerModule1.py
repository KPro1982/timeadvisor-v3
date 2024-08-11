import anvil.server
import csv
import pandas as pd
import json
import anvil.media


# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#

  
@anvil.server.callable
def SetClientData(file_name, file_object):
  print("Hello World")
 # ClientDict = pd.read_excel(client_data)
 # print(ClientDict)
  

  