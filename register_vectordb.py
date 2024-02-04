################################################################################
# Name:
#   Simple register collection program on vector database
# Description:
#   This is sample program for register collection on vector database
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
#   python register_vecrotdb.py
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
# defined sentence transformer LLM
sentence_transformer_ef = \
    embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="intfloat/multilingual-e5-large")

################################################################################
# get or create collection
collection = client.get_or_create_collection(
    CHROMA_SERVER_VECTORDB_COLLECTION,
    embedding_function=sentence_transformer_ef
)

################################################################################
# Changing the distance function to the Cosine Similarity
# Chroma uses Euclidean distance as the algorithm for measuring the distance 
#  between vectors by default.
# In this sample program, we use HNSW(Hierarchical Navigable Small World),
#  an ANN(Approximate Nearest Neighbor search) algorithm, for measuring 
#  the distance between vectors. 
# We use cosine similarity for the Distance Metrics, a similarity distance 
#  calculation algorithm.
# For more ditails,pelase reffer to chroma official document section
#  Changing the distance function
#  https://docs.trychroma.com/usage-guide#changing-the-distance-function
collection.modify(metadata={"hnsw:space": "cosine"})

################################################################################
# Add collection items to vector database
collection.add(
    documents=["ある日、スーパーサラリーマンだった“ツレ”が「死にたい！」ってつぶやいた！　一体どうしちゃったのツレ？　“ツレ”がうつ病になったことがきっかけで、成長していく夫婦の姿を描いた大人気・コミックエッセイ「ツレがうつになりまして。」。とかく暗くなりがちなうつ病というテーマをユーモアたっぷりにアッケラカンと吹き飛ばす原作の良さをそのままに、宮崎あおい＆堺雅人のコンビで待望の映画化を果たした。難しいテーマであるうつ病をほんわかハッピーに演じきった二人は、大河ドラマ「篤姫」続き、二度目の夫婦コンビ。今回は、撮影秘話や演じた夫婦役についてじっくりと話をうかがった。",
               "今や全国区の人気を誇る“ブサかわ”秋田犬・わさお。今年3月には本人出演による主演映画『わさお』にてスクリーン・デビューを果たした「わさお」と、10代・20代の若者に人気のロックバンドthe pillowsのボーカル「山中さわお」が、奇跡の対面を果たした。今年2月上旬頃から、自身のラジオ番組で「わさおという犬がいる」というメールがよく届くようになり、わさおの存在を徐々に気になりだしていた山中さわお。2月18日より開始したthe pillows HORN AGAIN TOURのMC中に、山中さわおが「わさおというブサカワ犬がいるじゃないか？一回会ってみたいんだよね」と話すと、ファンがmixiやツイッターなどで騒ぎ出し、それを耳にしたわさおの関係者も「いつかコラボレーションができたら面白いですね」と話すようになった。",
               "芸能界一のリアクション芸人として名高い上島竜兵が、日頃からいじられ続けることに関して不満を持ち「もう肥後、ジモンの指図は受けない！ おでんも食わないし、熱湯風呂にも入らない!!」と逆襲を宣言。極秘実験「スーパーソルジャー計画」に参加して、自らの肉体を変えることを志願した。これは、10月14日公開の『キャプテン・アメリカ/ザ・ファースト・アベンジャー』の記念イベント。劇中では、貧弱だが人一倍正義感が強い主人公スティーブ・ロジャースが、軍の秘密実験“スーパーソルジャー”計画に参加し、身長、筋力、脚力、跳躍力を飛躍的に進化させ、善良な人格も極限までに増幅させたスーパーヒーロー“キャプテン・アメリカ”となる。"],
    metadatas=[
				{"url": "http://news.livedoor.com/article/detail/5840081/",
                 "title": "インタビュー：宮崎あおい＆堺雅人「一緒にいるのが当たり前」",
                 "chunk": "1",
                 "date": "2011-09-08T10:00:00+0900"},
				{"url": "http://news.livedoor.com/article/detail/5840350/",
                 "title": "「さわお」×「わさお」が奇跡の対面",
                 "chunk": "1",
                "date": "2011-09-06T16:25:00+0900"},
				{"url": "http://news.livedoor.com/article/detail/5840524/",
                "title": "上島竜兵が「出川には負けない！」と極秘実験でイケメンマッチョに変身",
                "chunk": "1",
                "date": "2011-09-06T17:32:00+0900"}
		],
    ids=[       "1",
                "2",
                "3"
    ]
)