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
def Process_Msg(name):
  newname = name + "- Changed it"
  return newname

@anvil.server.callable
def MakeXL(data):
    df = pd.json_normalize(data, max_level=0)
    print(df)
    file_name = 'TimeEntryData.xlsx'
    datatoexcel = pd.ExcelWriter(file_name)
    df.to_excel(file_name)
    return anvil.media.from_file(file_name)