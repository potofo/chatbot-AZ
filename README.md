# chatbot-AZ - Simple Chatbot program for Azure OpenAI Service

![chatbot-AZ_test](https://github.com/potofo/chatbot-AZ/assets/138992835/2590fd0f-14f7-47a2-9040-78e66f425d2c)


## Description
This is a sample program designed to help inexperienced programmers learn how to use the Azure OpenAI Service API. It demonstrates how to interact with the OpenAI Chat Completion API and handle conversation persistence.

## Specifications of the Chatbot

- The tokens include the last 5 conversations between the user and the assistant, including the latest one. This ensures continuity of the conversation and makes it appear as if the conversation is ongoing.
- The system prompt is fixed as follows:

```python
**As an experienced engineer, you will step-by-step consider complex technical problems, answer questions and provide advice.**

```

- The token limit size for the prompt is set to 800 tokens in the API instructions. If this limit is exceeded, an error is expected.
- API calls are intended to be asynchronous, with the response messages being streamed in real-time to the response container in Streamlit. However, there is a bug that prevents displaying while communicating asynchronously.

## Installation
The prerequisite packages for chatbot-AZ are listed in requirements.txt after normalization. Please install them with the following pip install command.
**pip install -r requirements.txt**
It is recommended to build a Python virtual environment (python -m venv venv) as your execution environment.
```shell
(venv) D:\Python\chatbot-AZ>pip install -r requirements.txt
Collecting openai==0.27.8 (from -r requirements.txt (line 1))
  Using cached openai-0.27.8-py3-none-any.whl.metadata (13 kB)
Collecting streamlit==1.27.1 (from -r requirements.txt (line 2))
  Using cached streamlit-1.27.1-py2.py3-none-any.whl.metadata (8.0 kB)
Collecting python-dotenv==1.0.0 (from -r requirements.txt (line 3))
  Using cached python_dotenv-1.0.0-py3-none-any.whl (19 kB)
...
Using cached smmap-5.0.1-py3-none-any.whl (24 kB)
Installing collected packages: pytz, zipp, watchdog, validators, urllib3, tzdata, typing-extensions, tornado, toolz, toml, tenacity, smmap, six, rpds-py, python-dotenv, pygments, protobuf, pillow, packaging, numpy, multidict, mdurl, MarkupSafe, idna, frozenlist, colorama, charset-normalizer, certifi, cachetools, blinker, attrs, async-timeout, yarl, tzlocal, tqdm, requests, referencing, python-dateutil, pyarrow, markdown-it-py, jinja2, importlib-metadata, gitdb, click, aiosignal, rich, pydeck, pandas, jsonschema-specifications, gitpython, aiohttp, openai, jsonschema, altair, streamlit
Successfully installed MarkupSafe-2.1.5 aiohttp-3.9.3 aiosignal-1.3.1 altair-5.2.0 async-timeout-4.0.3 attrs-23.2.0 blinker-1.7.0 cachetools-5.3.2 certifi-2024.2.2 charset-normalizer-3.3.2 click-8.1.7 colorama-0.4.6 frozenlist-1.4.1 gitdb-4.0.11 gitpython-3.1.41 idna-3.6 importlib-metadata-6.11.0 jinja2-3.1.3 jsonschema-4.21.1 jsonschema-specifications-2023.12.1 markdown-it-py-3.0.0 mdurl-0.1.2 multidict-6.0.5 numpy-1.26.3 openai-0.27.8 packaging-23.2 pandas-2.2.0 pillow-10.2.0 protobuf-4.25.2 pyarrow-15.0.0 pydeck-0.8.1b0 pygments-2.17.2 python-dateutil-2.8.2 python-dotenv-1.0.0 pytz-2024.1 referencing-0.33.0 requests-2.31.0 rich-13.7.0 rpds-py-0.17.1 six-1.16.0 smmap-5.0.1 streamlit-1.27.1 tenacity-8.2.3 toml-0.10.2 toolz-0.12.1 tornado-6.4 tqdm-4.66.1 typing-extensions-4.9.0 tzdata-2023.4 tzlocal-5.2 urllib3-2.2.0 validators-0.22.0 watchdog-3.0.0 yarl-1.9.4 zipp-3.17.0
```

## How to Execute
Execute using the following streamlit command. When executed, a browser will launch.
Run `streamlit run chatbot-AZ.py --server.port 80`.

```shell
(venv) D:\Python\chatbot-AZ>streamlit run chatbot-AZ.py --server.port 80

  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:80
  Network URL: http://192.168.1.137:80

dotenv_path:Q:\OneDrive\Python\chatbot-AZ\.env
Not Found list_message key in session status
[{'content': 'As an experienced engineer, you play the role of thinking '
             'through complex technical issues step by step, answering '
             'questions, and providing advice.',
  'role': 'system'}]
```
This command is used to run the `chatbot-AZ.py` script with `streamlit`, on port 80.

## Code explanation
This code is a simple chatbot program for Azure OpenAI Service. Here is an explanation of the different sections of the code:

- Import sections: This section imports the necessary modules and packages for the program, including openai, streamlit, and pprint (for debugging).

- Global definitions: This section defines global variables and constants used in the program, such as the maximum number of messages, the Azure OpenAI API parameters, the deployment ID, and the system prompt.

- Global Variables definitions: This section defines two dictionaries, 'dict_message' and 'dict_response', which are used to store the user input messages and the chatbot responses respectively.

- Specify Azure OpenAI API parameters: This section sets the necessary parameters for the Azure OpenAI API, including the API type, API key, API host, and API version.

- Screen Layout definitions: This section defines the layout of the chatbot interface using streamlit container elements. It includes containers for the response messages and the user input.

- First Message: This section displays the first message from the chatbot in the response container.

- form to container_input definitions: This section creates a form to capture the user's input prompt in the input container.

- Restore list_messages from session state: This section checks if the list_messages variable exists in the session state (which persists across multiple interactions with the chatbot). If it exists, it restores the previous messages. Otherwise, it sets the initial system prompt message and saves it in the session state.

- Event Dispatcher: This section handles the event when the user enters a prompt. It adds the user's prompt to the list of messages, displays all the messages in the response container, sends the messages to the Azure OpenAI Chat Completion API, and receives the completion in chunks. It then appends the chatbot's response to the list of messages, purges old messages if necessary, and saves the updated list of messages in the session state for future interactions.

Note: This code is specifically designed to work with Azure OpenAI Service and Streamlit. It leverages the capabilities of these services to create a simple chatbot interface.

![chatbot-AZ_screen](https://github.com/potofo/chatbot-AZ/assets/138992835/06a0c3f6-ccf0-490e-88f4-fdf5cba2cae5)

## Requirements
- Azure OpenAI Service:
  - You will need an Azure OpenAI endpoint, API key, and API version for this program to work.
  - A subscription to the pay-as-you-go Azure OpenAI Service is required for key issuance.
- openai package (Ver 0.27.8):
  - This program uses the `openai` package to interact with the OpenAI API.
- Streamlit:
  - The program requires Streamlit version 1.24.0 or higher to use `streamlit_chat`.
- python-dotenv:
  - The program requires python-dotenv version 1.0.0 or higher to use get environment valiables.

## Establish OpenAI key on Azure OpenAI Service
Here is the process for issuing an API in Azure OpenAI Service:

1. Log in to the Azure portal.
2. Create a resource group.
3. Create Azure OpenAI Service within the resource group.
4. Deploy LLM in Azure OpenAI Studio.
5. Return to Azure OpenAI Service and retrieve the necessary information
   (Endpoint, API key, API version).

This is the process for issuing an API in Azure OpenAI Service. For detailed instructions, please refer to the official Azure documentation.

## Author
- potofo

## Revision
- 2023/09/30 01-00 potofo: Initial Creation.
- 2023/10/01 01-01 portfo: Fixed incremental response from assistant.
- 2023/10/06 01-02 portfo: Consider parameterizing for Azure App Service and environment variables.

## Disclaimer
Please be aware that we are not responsible for any problems caused by this program.

## Restrictions
-

## License
- MIT License

## Copyright
- Copyright (c) 2023 potofo. All rights reserved.

## Note
-
