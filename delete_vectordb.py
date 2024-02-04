################################################################################
# Name:
#   Simple delete collection program on vector database
# Description:
#   This is sample program for delete collection on vector database
# Requirement:
#   chroma
#     This is the server program for the vector database used in this program.
#     This time, it's a 1024-dimension vector data using 
#      intfloat/multilingual-e5-large in sentence transformer(LLM).
#     Also, the distance function between vectors uses Cosine Similarity.
#     For more details, please refer to the code in register_vectordb.py.
# Auther:
#   potofo
# Revision:
#   2024/02/04 01-00 potofo   Initial Creation.
# How to execut:
#   python delete_vectordb.py
# Disclaimer:
#   Please be aware that we are not responsible for any problems caused by this 
#   program.
# Restriction:
#   -
# License:
#   MIT License
# Copyright:
#   Copyright (C) 2024 potofo. All rihtts reserved.
# Note:
#   -
################################################################################
# Import sections
import chromadb                      # for Chroma vectordb
from chromadb.config import Settings # for Chroma vectordb
import os                            # for Get Environment Valiables
from os.path import join, dirname    # for establish path
from dotenv import load_dotenv       # for Loading .env file

# Get Environment Variables
load_dotenv(verbose=True)
dotenv_path = join(dirname(__file__), '.env')
print(f'dotenv_path:{dotenv_path}')
load_dotenv(dotenv_path)

################################################################################
# Global definitions
# Storing the information of the connecting vector database in a variable.
CHROMA_SERVER                     = \
    os.environ.get('CHROMA_SERVER','localhost')
CHROMA_SERVER_PORT                = \
    int(os.environ.get('CHROMA_SERVER_PORT',8080))
CHROMA_SERVER_AUTH_CREDENTIALS    = \
    os.environ.get('CHROMA_SERVER_AUTH_CREDENTIALS','secret_credentials')
CHROMA_SERVER_VECTORDB_COLLECTION = \
    os.environ.get('CHROMA_SERVER_VECTORDB_COLLECTION','EVALRAG')

print(f'CHROMA_SERVER                    :{CHROMA_SERVER}')
print(f'CHROMA_SERVER_PORT               :{str(CHROMA_SERVER_PORT)}')
print(f'CHROMA_SERVER_AUTH_CREDENTIALS   :{CHROMA_SERVER_AUTH_CREDENTIALS}')
print(f'CHROMA_SERVER_VECTORDB_COLLECTION:{CHROMA_SERVER_VECTORDB_COLLECTION}')

################################################################################
# Connect vector database
try:
    # Without authentifications
    #client = chromadb.HttpClient(
    #    host=CHROMA_SERVER,
    #    port=CHROMA_SERVER_PORT)

    # With authentifizations
    client = chromadb.HttpClient(
        host=CHROMA_SERVER,
        port=CHROMA_SERVER_PORT,
        settings=Settings(
            chroma_client_auth_provider='chromadb.auth.token.TokenAuthClientProvider',
            chroma_client_auth_credentials=CHROMA_SERVER_AUTH_CREDENTIALS)
        )
except Exception as e:
    print('Vector database Connection error occurs with following message.')
    print('Error Message:{0}'.format(str(e)))
    sys.exit(-1)

################################################################################
# Global definitions
client.delete_collection(CHROMA_SERVER_VECTORDB_COLLECTION)