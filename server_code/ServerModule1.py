import anvil.secrets
import anvil.server
import csv
import pandas as pd
import json
import anvil.media

from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import OutlookMessageLoader
from langchain_community.chat_models import ChatOpenAI
from langchain_community.llms import openai
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter


# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#

clientDict = ""
aliasesList = ""
matterList = ""


  
@anvil.server.callable
def MakePanda(data):
  global df 
  df = pd.json_normalize(data)
  print(type(df))
  file_name = 'TimeEntryData.xlsx'
  datatoexcel = pd.ExcelWriter(file_name)
  df.to_excel(file_name, columns=['userId','timekeepr','client','matter','task','activity','billable','hoursWorked','hoursBilled','rate','amount','narrative','alias','length','subject','bcc','body', 'cc','date','filename','messageId','recipients','sender'])  # 
  return anvil.media.from_file(file_name)
  
  
def generateClientAlias(docs):
    gloabal df
    llm = ChatOpenAI(temperature=0.3, model_name="gpt-3.5-turbo-16k", api_key=anvil.secrets.get_secret('OPENAI_API_KEY'))
    AliasesString = aliasesList.__str__()
    df = df.reset_index() 
  
    for index, row in df.iterrows():
      print(row['Name'], row['Client/Matter'])
  
@anvil.server.callable
def SetClientData(file_object):
  global clientDict
  print("Client_Data_Processing")
  clientDict = pd.read_excel(file_object.get_bytes())
  GetAliasesList()
  GetMatterNumberList()
  

 

def GetAliasesList():
    global clientDict
    global aliasesList  

    aliasesList = clientDict['Name'].to_list()
    aliasesList.insert(0,"None")
  
def GetMatterNumberList():
  global clientDict
  global matterList
  matterList = clientDict['Client/Matter Number'].to_list()
  matterList.insert(0,"None")

  def generateClientAlias():
    llm = ChatOpenAI(temperature=0.3, model_name="gpt-3.5-turbo-16k", api_key=anvil.secrets.get_secret('OPENAI_API_KEY'))
    AliasesString = aliasesList

    for index, row in df.iterrows():
      print(row['Name'], row['Client/Matter'])

@anvil.server.callable
def Process(data, file_object):
  MakePanda(data)
  SetClientData(file_object)
  generateClientAlias("Alvarez v. Command Security Services")
   