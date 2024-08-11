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

def generateClientAlias(docs):
    llm = ChatOpenAI(temperature=0.3, model_name="gpt-3.5-turbo-16k", api_key=anvil.secrets.get_secret('OPENAI_API_KEY'))
    AliasesString = aliasesList.__str__()
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
    print(output)
  
@anvil.server.callable
def SetClientData(file_name, file_object):
  global clientDict
  print("Client_Data_Processing")
  clientDict = pd.read_excel(file_object.get_bytes())
  GetAliasesList()
  GetMatterNumberList()

  generateClientAlias("Alvarez v. Command Security Services")

def GetAliasesList():
    global clientDict
    global aliasesList
    clientData = clientDict
    aliasesList = clientData.to_dict('list')['Name']
    aliasesList.insert(0,"None")
    print(aliasesList)
  
def GetMatterNumberList():
  global clientDict
  global matterList
  clientData = clientDict
  matterList = clientData.to_dict('list')['Client/Matter Number']
  matterList.insert(0,"None")
  print(matterList)
   
  # return matterList
  def generateClientAlias(docs):
    llm = ChatOpenAI(temperature=0.3, model_name="gpt-3.5-turbo-16k", api_key=anvil.secrets.get_secret('OPENAI_API_KEY'))
    AliasesString = aliasesList
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
    print(output)