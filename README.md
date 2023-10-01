# chatbot-AZ - Simple Chatbot program for Azure OpenAI Service

![chatbot-AZ_test](https://github.com/potofo/chatbot-AZ/assets/138992835/b860ca17-c546-40cb-835f-e5d0331d0b5b)

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

## Requirements
- Azure OpenAI Service:
  - You will need an Azure OpenAI endpoint, API key, and API version for this program to work.
  - A subscription to the pay-as-you-go Azure OpenAI Service is required for key issuance.
- openai package (Ver 0.27.8):
  - This program uses the `openai` package to interact with the OpenAI API.
- Streamlit:
  - The program requires Streamlit version 1.24.0 or higher to use `streamlit_chat`.

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
