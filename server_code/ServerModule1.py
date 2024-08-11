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
@anvil.server.callable
def Process_Msg(name):
  newname = name + "- Changed it"
  return newname

@anvil.server.callable
def MakeXL(data):
    file_name = 'TimeEntryData.xlsx'
    datatoexcel = pd.ExcelWriter(file_name)
    df.to_excel(file_name, columns=['userId','timekeepr','client','matter','task','activity','billable','hoursWorked','hoursBilled','rate','amount','narrative','alias','length','subject','bcc','body', 'cc','date','filename','messageId','recipients','sender'])
    return anvil.media.from_file(file_name)

def MakePanda(data):
  df = pd.json_normalize(data)
  print(df)

def SetClientData(client_data):
  ClientDict = pd.read_excel(client_data)
  print(ClientDict)
def GetClientData():
    data_path = st.session_state.local_folder + "clientdata.xlsx"
    ClientDict = pd.read_excel(data_path)
    return ClientDict

def GetClientDictionary():
    clientData = GetClientData()
    clientDict = clientData.to_dict('split')['data']
    return clientDict

def GetAliasesList():
    clientData = GetClientData()
    aliasesList = clientData.to_dict('list')['Name']
    aliasesList.insert(0,"None")
    return aliasesList

def GetMatterNumberList():
    clientData = GetClientData()
    matterList = clientData.to_dict('list')['Client/Matter Number']
    matterList.insert(0,"None")
    return matterList


def GetAliasesString():
    AliasesList = GetAliasesList()
    delimiter = ", "
    return delimiter.join(AliasesList)

def generateClientAlias(docs):
    llm = ChatOpenAI(temperature=0.3, model_name="gpt-3.5-turbo-16k")
    AliasesString = GetAliasesString()

# Define template

    template_string = """
    You are an attorney billing expert. Your job is to infer the client alias from the folowing email: {text} 
    
    In most cases, the subject of the email will contain the alias. In those cases you will compare the email subject with the LIST OF APPROVED ALIASES and return the alias FROM THE LIST OF APPROVED ALIASES that best matches the subject line. 

    For example, where the email subject is "topix -- quick questions", you would compare this to the list of approved aliases and infer that Page v. Topix Pharmaceuticals is the best fit for the alias because none of the other aliases contain the work topix.
    
    In some cases, the subject will not contain enough information to infer the alias. In those case, you will look at the body of the email for information that matches an alias FROM THE LIST OF APPROVED ALIASES. 
    Example 1: you may infer the  alias: Page v. Topix Pharmaceuticals where the body of the email refers to a person named Page. 
    Example 2: you may infer the alias: Aguilera v. Turner Systems, Inc. where the subject of the email refers to Turner.

    IMPORTANT: YOUR RESPONSE SHOULD NOT BE CONVERSATIONAL. YOUR REPSONSE ONLY CONTAIN THE ALIAS FROM THE LIST OF APPROVED ALIASES WITHOUT ANY ADDITIONAL WORDS. 

    INCORRECT response: Based on the information provided in the email, the inferred client alias is "Gonzalez v. DS Electric, Inc."
    CORRECT response: Gonzalez v. DS Electric, Inc.

    IMPORTANT: IF YOU CANNOT INFER AN ALIAS FROM THE CONTENT PROVIDED, YOUR MUST RESPOND WITH THE SINGLE WORD: None

    INCORRECT response: The inferred client alias from the email is None.
    CORRECT response: none

    THE LIST OF APPROVED ALIASES FOLLOWS = """ + AliasesString 




    prompt = PromptTemplate.from_template(template_string)
    
    chain = load_summarize_chain(llm, chain_type="stuff", prompt=prompt)
    output_clientmatter = chain.run(docs)
    output = output_clientmatter.strip()
    return output