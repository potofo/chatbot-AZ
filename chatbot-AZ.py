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
# Disclaimer:
#   Please be aware that we are not responsible for any problems caused by this 
#   program.
# Restriction:
#   -
# License:
#   MIT License
# Copyright:
#   Copyright (c) 2023 potofo. All rihtts reserved.
# Note:
#   -
################################################################################
# Import sections
import openai                     # 0.27.8
import streamlit as st            # must be 1.24.0 or higher
import pprint                     # for debug to confirm message internal scheme
import os                         # for Get Environment Valiables
from os.path import join, dirname # for establish path
from dotenv import  load_dotenv   # for Loading .env file

# Get Environment Variables
load_dotenv(verbose=True)
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Global definitions
# for example
# MAX_MESSAGES        = 5
# OPENAI_API_TYPE     = 'azure'
# OPENAI_API_KEY      = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
# OPENAI_API_HOST     = 'https://xxxxxxxx.openai.azure.com/'
# OPENAI_API_VERSION  = '2023-07-01-preview'
# AZURE_DEPLOYMENT_ID = 'gpt-35-turbo'
# SYSTEM_PROMPT       = 'As an experienced engineer, you will step-by-step' \
#                       ' consider complex technical problems, answer' \
#                       '  questions,and provide advice.'
MAX_MESSAGES        = int(os.environ.get('MAX_MESSAGES',5))
OPENAI_API_TYPE     = os.environ.get('OPENAI_API_TYPE','azure')
OPENAI_API_KEY      = os.environ.get('OPENAI_API_KEY')
OPENAI_API_HOST     = os.environ.get('OPENAI_API_HOST')
OPENAI_API_VERSION  = os.environ.get('OPENAI_API_VERSION','2023-07-01-preview')
# The AZURE_DEPLOYMENT_ID is the name of the LLM deployed with
# Azure OpenAI Service
AZURE_DEPLOYMENT_ID = os.environ.get('AZURE_DEPLOYMENT_ID','gpt-35-turbo')
# SYSTEM_PROMPT
SYSTEM_PROMPT       = os.environ.get('SYSTEM_PROMPT',
                      'As an experienced engineer, you will step-by-step' \
                      ' consider complex technical problems, answer questions,' \
                      ' and provide advice.'
                      )

# Global Valiables definitions
list_messages = []
dict_message  = {}
dict_response = {}

# Specify Azure OpenAI API parameters
openai.api_type    = OPENAI_API_TYPE
openai.api_base    = OPENAI_API_HOST
openai.api_version = OPENAI_API_VERSION
openai.api_key     = OPENAI_API_KEY

################################################################################
# Screen Layout definitions
# Layout is implemented with streamlit container elements.
container_response = st.container()
container_input    = st.container()

# First Message
block_first_message = container_response.chat_message('assistant')
block_first_message.write('This is ChatGPT,May I help you?')

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
    dict_message['content']  = prompt
    dict_message['role']     = 'user'
    list_messages.append(dict_message)

    # Output system prompts and prompts from User in response container.
    for message in list_messages:
        block_message = container_response.chat_message(message['role'])
        block_message.write(message['content'])

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
            async_message.write(response_agent)

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
