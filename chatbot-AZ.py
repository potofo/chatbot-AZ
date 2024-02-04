################################################################################
# Name:
#   Simple Chatbot program for Azure OpenAI Service
# Description:
#   This is sample program for learning Open API for inexperienced programmers.
# Requirement:
#   about Azure OpenAI Service
#     You will need an Azure OpenAI endpoint, API key, and API version for this
#     program to work.
#     A subscription to the pay-as-you-go Azure OpenAI Service is required for
#     key issuance.
#   openai
#     Using the openai package(Ver 0.27.8) to use the OpenAI API
#   Streamlit
#     To use streamlit_chat, the streamlit version must be 1.24.0 or higher.
# Auther:
#   potofo
# Revision:
#   2023/09/30 01-00 potofo   Initial Creation.
#   2023/10/01 01-01 portfo   Fixed incremental response from assustant.
#   2023/10/06 01-02 portfo   Consider parameterizing for Azure App Service
#                             and environment variables.
#   2024/02/03 01-02 portfo   Changed OPENAI_API_VERSION to latest.
#   2024/02/03 01-03 portfo   Added RAG capabilities.
# How to execut:
#   streamlit run chatbot-AZ.py
# Disclaimer:
#   Please be aware that we are not responsible for any problems caused by this 
#   program.
# Restriction:
#   -
# License:
#   MIT License
# Copyright:
#   Copyright (C) 2023-2024 potofo. All rihtts reserved.
# Note:
#   -
################################################################################
# Import sections
import openai                        # 0.27.8
import streamlit as st               # must be 1.24.0 or higher
import pprint                        # for debug to confirm message internal scheme
import os                            # for Get Environment Valiables
from os.path import join, dirname    # for establish path
from dotenv import load_dotenv       # for Loading .env file
import chromadb                      # for Chroma vectordb
from chromadb.config import Settings # for Chroma vectordb
from chromadb.utils import embedding_functions

# Get Environment Variables
load_dotenv(verbose=True)
dotenv_path = join(dirname(__file__), '.env')
print(f'dotenv_path:{dotenv_path}')
load_dotenv(dotenv_path)

# Global definitions
# for example
# MAX_MESSAGES        = 5
# OPENAI_API_TYPE     = 'azure'
# OPENAI_API_KEY      = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
# OPENAI_API_HOST     = 'https://xxxxxxxx.openai.azure.com/'
# OPENAI_API_VERSION  = '2023-12-01-preview'
# Note about API VERSION
# Azure officially announced on January 17, 2023, that the following
#  API versions will be discontinued on April 2, 2024.
# 2023-03-15-preview
# 2023-06-01-preview
# 2023-07-01-preview
# 2023-08-01-preview
# As of February 3, 2024, the latest API version is 2023-12-01-preview. 

# https://learn.microsoft.com/ja-jp/azure/ai-services/openai/api-version-deprecation
# AZURE_DEPLOYMENT_ID = 'gpt-35-turbo'
# SYSTEM_PROMPT       = 'As an experienced engineer, you will step-by-step' \
#                       ' consider complex technical problems, answer' \
#                       '  questions,and provide advice.'
MAX_MESSAGES        = int(os.environ.get('MAX_MESSAGES',5))
OPENAI_API_TYPE     = os.environ.get('OPENAI_API_TYPE','azure')
OPENAI_API_KEY      = os.environ.get('OPENAI_API_KEY')
OPENAI_API_HOST     = os.environ.get('OPENAI_API_HOST')
OPENAI_API_VERSION  = os.environ.get('OPENAI_API_VERSION','2023-12-01-preview')
# The AZURE_DEPLOYMENT_ID is the name of the LLM deployed with
# Azure OpenAI Service
AZURE_DEPLOYMENT_ID = os.environ.get('AZURE_DEPLOYMENT_ID','gpt-35-turbo')
# SYSTEM_PROMPT
SYSTEM_PROMPT       = os.environ.get('SYSTEM_PROMPT',
                      'You are an excellent secretary. ' \
                      ' Please think about any problem step-by-step and ' \
                      ' give good advice to the questioner.'
                      )

PROMPT_TEMPLATE     = os.environ.get('PROMPT_TEMPLATE',
                      '##### Please answer the following question from the context.  \n' \
                      'Question:{prompt}  \n' \
                      'Context:  \n' \
                      '{context}\n'
                      )
CHROMA_SERVER                     = \
    os.environ.get('CHROMA_SERVER','localhost')
CHROMA_SERVER_PORT                = \
    int(os.environ.get('CHROMA_SERVER_PORT',8080))
CHROMA_SERVER_AUTH_CREDENTIALS    = \
    os.environ.get('CHROMA_SERVER_AUTH_CREDENTIALS','secret_credentials')
CHROMA_SERVER_VECTORDB_COLLECTION = \
    os.environ.get('CHROMA_SERVER_VECTORDB_COLLECTION','EVALRAG')
CHROMA_SERVER_NUMBER_OF_RESULT = \
    int(os.environ.get('CHROMA_SERVER_NUMBER_OF_RESULT','10'))
CHROMA_DISTANCE_THRESHOLD = \
    float(os.environ.get('CHROMA_DISTANCE_THRESHOLD','0.40'))

# Global Valiables definitions
list_messages = []
dict_message  = {}
dict_response = {}

# Specify Azure OpenAI API parameters
openai.api_type     = OPENAI_API_TYPE
openai.api_base     = OPENAI_API_HOST
openai.api_version  = OPENAI_API_VERSION
openai.api_key      = OPENAI_API_KEY

################################################################################
# Connect Vector Database
def connect_vectordb(chroma_server,chroma_server_port,chroma_credentials):
    print('>>connect_vectordb')
    # With authentifizations
    client = chromadb.HttpClient(
        host=chroma_server,
        port=chroma_server_port,
        settings=Settings(
            chroma_client_auth_provider='chromadb.auth.token.TokenAuthClientProvider',
            chroma_client_auth_credentials=chroma_credentials
        )
    )
    return client

################################################################################
# Query Vector Database
def query_vectordb(client,collection,prompt,n_results):
    print('>>query_vectordb')
    sentence_transformer_ef = \
        embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="intfloat/multilingual-e5-large"
        )
    collection = client.get_collection(
        name=collection,
        embedding_function=sentence_transformer_ef
    )

    results = collection.query(
        query_texts=prompt,
        n_results=n_results,
        #include=['documents', 'distances', 'metadatas','embeddings']
        include=['documents', 'distances', 'metadatas']
    )
    print('number of results:{0}'.format(str(len(results['ids']))))
    
    return results

################################################################################
# Connect Vector Database
chroma_server      = CHROMA_SERVER
chroma_server_port = CHROMA_SERVER_PORT
chroma_credentials = CHROMA_SERVER_AUTH_CREDENTIALS
client = connect_vectordb(chroma_server,chroma_server_port,chroma_credentials)

################################################################################
# Screen Layout definitions
# Layout is implemented with streamlit container elements.
block_sidebar_title   = st.sidebar.empty()
block_sidebar_reset   = st.sidebar.empty()
block_ragswitch       = st.sidebar.empty()
block_prompt_template = st.sidebar.empty()
prompt_tamplate       = st.empty()
container_response    = st.container()
container_input       = st.container()

# Sidebar description
sidebar_title         = block_sidebar_title.markdown('# **Chatbot-AZ**')
sidebar_resetbutton   = block_sidebar_reset.button('Reset conversation')
sidebar_ragswitch     = block_ragswitch.radio('RAG(Retrieval-Augmented Generation) Switch', \
                                                ('On','Off'), \
                                                horizontal=True)
sidebar_prompt_tamplate = block_prompt_template.text_area(label='Prompt Template',value=PROMPT_TEMPLATE,height=600)

# First Message
block_first_message = container_response.chat_message('assistant')
block_first_message.markdown('This is ChatGPT,May I help you?')

# form to container_input definitions
prompt = container_input.chat_input('prompt')

# Restore list_messages from session state
if 'list_messages' in st.session_state:
    print('Restore list_message valiable successful from session status!!')
    list_messages = st.session_state['list_messages']
else:
    print('Not Found list_message key in session status')
    # Set System prompt
    dict_message['content']  =  SYSTEM_PROMPT
    dict_message['role']     = 'system'
    list_messages.append(dict_message)
    pprint.pprint(list_messages)
    # Save Session state
    st.session_state['list_messages'] = list_messages

################################################################################
# Event Dispatcher
if(prompt):
    # User prompt input event
    print(f'Detect user prompt input event (prompt:{prompt})')

    # Establish message to OpenAI Chat Completion API
    if sidebar_ragswitch == 'On':
        # RAG
        collection = CHROMA_SERVER_VECTORDB_COLLECTION
        n_results  = CHROMA_SERVER_NUMBER_OF_RESULT
        results = query_vectordb(client,collection,prompt,n_results)

        #import pprint
        #pprint.pprint(results['documents'][0][0],indent=2)

        # include all results data
        context = ''
        # document
        distance_threshold = CHROMA_DISTANCE_THRESHOLD
        for i in range(len(results['ids'])-1, -1, -1):
            if results['distances'][i][0] < distance_threshold:
                context += '  \n' + results['documents'][i][0]

        # establish prompt
        prompt_context = '  ' + PROMPT_TEMPLATE
        prompt_context = prompt_context.replace('{prompt}',prompt)
        prompt_context = prompt_context.replace('{context}',str(context))
        sidebar_prompt_tamplate = block_prompt_template.text_area(label='Generated Prompt',value=prompt_context,height=600)
        dict_message['content']  = prompt_context
    else:
        dict_message['content']  = prompt
    dict_message['role']     = 'user'
    list_messages.append(dict_message)

    # Output system prompts and prompts from User in response container.
    for message in list_messages:
        block_message = container_response.chat_message(message['role'])
        block_message.markdown(message['content'])

    # Send message to LLM with conversation persistence maintained.
    # The stream parameter specifies asynchronous communication
    completion = openai.ChatCompletion.create(
        deployment_id     = AZURE_DEPLOYMENT_ID,
        messages          = list_messages,
        stream            = True,
        temperature       = 0.7,
        max_tokens        = 800,
        top_p             = 0.95,
        frequency_penalty = 0,
        presence_penalty  = 0,
        stop              = None
    )

    result_area = st.empty()
    response_agent = ''

    # In case of the stream=True parameter is specified in the ChatCompletion.
    # create function, the completion is divided into chunks and received.
    block_message = container_response.chat_message('assistant')
    async_message = block_message.empty()

    for chunk in completion:
        if(chunk['id']):
            next = chunk['choices'][0]['delta'].get('content', '')
            response_agent += next
            async_message.markdown(response_agent)

    # Add reffer urls
    distance_threshold = CHROMA_DISTANCE_THRESHOLD
    if sidebar_ragswitch == 'On':
        # url, chunk, modify date
        response_agent += '  \n  \n'
        for i in range(len(results['ids'])-1, -1, -1):
            if results['distances'][i][0] < distance_threshold:
                response_agent += 'reffer:' + \
                    '[' + results['metadatas'][i][0]['title'] + '](' + \
                    results['metadatas'][i][0]['url'] + ')' +\
                    '(chunk:' + results['metadatas'][i][0]['chunk'] + ' ' + \
                     'LastUpdate:' + results['metadatas'][i][0]['date'] + ')' + \
                    '\n'
        async_message.markdown(response_agent)

    # Append Agent response to list_messages
    dict_response['role']  = 'assistant'
    dict_response['content']  = response_agent
    list_messages.append(dict_response)
    
    # Purge old list_massages without system prompt.
    num_messages = len(list_messages)
    print(f'num_messages:{num_messages}')
    pprint.pprint(list_messages)
    if(num_messages > (MAX_MESSAGES * 2 + 1)):
        # (user + assistant) x MAX_MESSAGES + system x 1
        del list_messages[1]
        del list_messages[1]

    # Save Session state
    # The streamlit is internally reloaded when it detects an event, 
    # list_message must be set to session_state.
    st.session_state['list_messages'] = list_messages

if(sidebar_resetbutton):
    # Purge all list_massages without system prompt.
    num_messages = len(list_messages)
    print(f'num_messages:{num_messages}')
    for i in range(0,num_messages-2):
        print(f'list_messages:{i}')
        del list_messages[1]
    st.session_state['list_messages'] = list_messages
    num_messages = len(list_messages)
    print(f'num_messages:{num_messages}')
