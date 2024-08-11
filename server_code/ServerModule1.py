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

ClientDict = ""
  
@anvil.server.callable
def SetClientData(file_name, file_object):
  global ClientDict
  print("Client_Data_Processing")
  ClientDict = pd.read_excel(file_object.get_bytes())
  GetMatterNumberList()
  GetAliasesList()

def GetAliasesList():
    global ClientDict
    clientData = ClientDict
    aliasesList = clientData.to_dict('list')['Name']
    aliasesList.insert(0,"None")
    print(aliasesList)
  
def GetMatterNumberList():
  global ClientDict
  clientData = ClientDict
  matterList = clientData.to_dict('list')['Client/Matter Number']
  matterList.insert(0,"None")
  print(matterList)
   
  # return matterList
  