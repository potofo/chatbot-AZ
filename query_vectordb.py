################################################################################
# Name:
#   Simple query collection program on vector database
# Description:
#   This is sample program for query collection on vector database
# Requirement:
#   chroma
#     This is the server program for the vector database used in this program.
#     This time, it's a 1024-dimension vector data using 
#      intfloat/multilingual-e5-large in sentence transformer(LLM).
#     Also, the distance function between vectors uses Cosine Similarity.
# Auther:
#   potofo
# Revision:
#   2024/02/04 01-00 potofo   Initial Creation.
# How to execut:
#   python query_vecrotdb.py
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
from chromadb.utils import embedding_functions
import sys                           # for sys.exit()
import os                            # for Get Environment Valiables
from os.path import join, dirname    # for establish path
from dotenv import load_dotenv       # for Loading .env file

# time
import time
#
import pandas as pd
from IPython.display import display

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
start = time.time()
try:
    # Without authentifications
    #client = chromadb.HttpClient(
    #    host='localhost',
    #    port=80)

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

end = time.time()
time_diff = end - start
spendding_time = round(time_diff,2)
print('connecting vecor database spendding {0} seconds.'.format(str(round(time_diff,3))))


################################################################################
# defined sentence transformer LLM
start = time.time()
sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="intfloat/multilingual-e5-large")

try:
    collection = client.get_collection(
        name=CHROMA_SERVER_VECTORDB_COLLECTION,
        embedding_function=sentence_transformer_ef
    )
except Exception as e:
    print(e)

end = time.time()
time_diff = end - start
spendding_time = round(time_diff,2)
print('connecting collection of vecor database spendding {0} seconds.'.format(str(round(time_diff,3))))

################################################################################
# defined user prompt
#prompt = "宮崎あおいが出演する映画を教えてください。"
#prompt = "ヴェネチア国際映画祭で金獅子賞を受賞した映画はなんですか？"
#prompt = "兎が出てくるホラー映画はなんですか？"
#prompt = "映画三銃士の主演女優の名前を教えてください。"
#prompt = "スリリングでかっこいいスパイ映画の名前とその映画の見どころを教えてください。"
#prompt = "子供向けのファンタジー映画で人気のある映画の名前とその映画の見どころを教えてください。"
prompt = "わさおの映画の見どころを教えてください。"
#prompt = "アップルの最新のOSの特徴を教えてください。"

################################################################################
# Query collection items from vector database by user prompt
start = time.time()
results = collection.query(
     query_texts=prompt,
     n_results=3,
     #include=['documents', 'distances', 'metadatas','embeddings']
     include=['documents', 'distances', 'metadatas']
)
end = time.time()
time_diff = end - start
spendding_time = round(time_diff,2)
print('query documents spendding {0} seconds.'.format(str(round(time_diff,3))))

################################################################################
# Filter queried collection items by distance threshold
#
# distance_threshold
# The score of the distance_threshold depends on the method of 
#  similarity measurement that is used.
# For example, in the case of cosine similarity, identical vectors will have 
#  a score of 0, whereas completely different vectors will have a score of 1.
# With other distance metrics, such as Euclidean distance, the scores can range
#  from 0 (the same point) to infinity.
# For example, if the distance_threshold is 0.35, it means that only those with
#  a confidence level of more than 65% will be filtered.
distance_threshold = 0.40

################################################################################
# Remove items from the collection that exceed the distance threshold
for ids, docs, distances, metas in zip(results['ids'], results['documents'], results['distances'], results['metadatas']):
    for i in range(len(ids)-1, -1, -1):
        if distances[i] > distance_threshold:
            # Remove items exceeding the distance_threshold
            ids.pop(i)
            docs.pop(i)
            distances.pop(i)
            metas.pop(i)

#print(results['ids'])
#print(results['metadatas'])

################################################################################
# Store in pandas dataframe
col_names = ['ids', 'url', 'chunk', 'title', 'distance']
#df = pd.DataFrame(columns=['ids', 'url', 'chunk'], ignore_index=False)
df = pd.DataFrame(columns=col_names)

for ids, docs, distances, metas in zip(results['ids'], results['documents'], results['distances'], results['metadatas']):
    for i in range(len(ids)-1, -1, -1):
        #print(metas)
        id       = ids[i]
        url      = metas[i]['url']
        chunk    = metas[i]['chunk']
        title    = metas[i]['title']
        dist     = distances[i]

        dict_row = {'ids': id, 'url': url, 'chunk': chunk, 'title': title, 'distance': dist}
        add_df   = pd.DataFrame([dict_row],columns=col_names)
        df       = pd.concat([df, add_df],axis=0).reset_index(drop=True)

################################################################################
# Display pandas dataframe
s = df.to_string(index=False,justify='left',max_colwidth=60)
print(s)

