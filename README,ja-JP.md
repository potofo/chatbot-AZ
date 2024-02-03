# chatbot-AZ - Azure OpenAIサービス用のシンプルなチャットボットプログラム

![chatbot-AZ_test ja-JP](https://github.com/potofo/chatbot-AZ/assets/138992835/a3de1c7a-8016-40ff-a6a1-9ffbbd5facaa)

## 説明
これは、経験が浅いプログラマーがAzure OpenAI Service APIの使い方を学ぶためのサンプルプログラムです。OpenAI Chat Completion APIとのインタラクションや会話の継続性の処理方法を示しています。

## チャットボットの仕様

- トークンには、ユーザとアシスタント間の最後の5回の会話が含まれています。これにより、会話の継続性が保証され、一貫した会話が続くかのような印象を与えます。
- システムプロンプトは以下のように固定されています:

```python
**経験豊富なエンジニアとして、複雑な技術問題を段階的に考慮し、質問に答え、アドバイスを提供します。**

```

- プロンプトのトークン制限サイズはAPIの指示に従って800トークンに設定されています。この制限を超えるとエラーが発生することが予想されます。
- API呼び出しは、非同期に行われ、応答メッセージがStreamlitのレスポンスコンテナにリアルタイムでストリーム化されることを前提としています。しかし、非同期通信中に表示できないバグが存在します。

## インストール
chatbot-AZの前提パッケージは正規化してrequirements.txtに記載してあります。
以下のpip installコマンドでインストールしてください。
**pip install -r requirements.txt**
実行環境はPython仮想環境(python -m venv venv)を構築することををお勧めします。

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

## 実行方法
以下のstreamlitコマンドで実行してください。実行するとブラウザが起動します。
**streamlit run chatbot-AZ.py --server.port 80**
```shell
(venv) Q:\OneDrive\Python\chatbot-AZ>streamlit run chatbot-AZ.py --server.port 80

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
このコマンドは、`streamlit`を使用して`chatbot-AZ.py`スクリプトをポート80で実行するために使用されます。

## コード説明
このコードは、Azure OpenAI Service用のシンプルなチャットボットプログラムです。以下は、コードの各セクションの説明です：

- インポートセクション: このセクションでは、プログラムに必要なモジュールとパッケージをインポートします。これにはopenai、streamlit、pprint（デバッグ用）などが含まれます。

- Global definitions:  このセクションでは、プログラムの中で使用されるグローバル変数と定数を定義しています。これには、メッセージの最大数、Azure OpenAI APIのパラメータ、デプロイメントID、システムプロンプトなどが含まれます。

- Global Variables definitions: このセクションでは、'dict_message'と'dict_response'という2つの辞書を定義しています。これらはユーザの入力メッセージとチャットボットの応答を保存するために使用されます。

- Specify Azure OpenAI API parameters: このセクションでは、Azure OpenAI APIの必要なパラメータを設定します。これにはAPIタイプ、APIキー、APIホスト、APIバージョンなどが含まれます。

- Screen Layout definitions: このセクションでは、streamlitのコンテナエレメントを使用してチャットボットインターフェースのレイアウトを定義します。これには、応答メッセージとユーザ入力のコンテナが含まれます。

- First Message: このセクションでは、チャットボットからの最初のメッセージをレスポンスコンテナに表示します。

- form to container_input definitions: このセクションでは、入力コンテナでユーザの入力プロンプトをキャプチャするためのフォームを作成します。

- Restore list_messages from session state: このセクションでは、list_messages変数がセッション状態(チャットボットとの複数回のインタラクションにまたがって持続)に存在するかどうかを確認します。存在する場合は以前のメッセージを復元し、存在しない場合は初期システムプロンプトメッセージを設定し、それをセッション状態に保存します。

- Event Dispatcher: このセクションでは、ユーザがプロンプトを入力したときのイベントを処理します。ユーザのプロンプトをメッセージリストに追加し、すべてのメッセージをレスポンスコンテナに表示し、メッセージをAzure OpenAI Chat Completion APIに送信し、完成部分をチャンクで受け取ります。生成したチャットボットの応答をメッセージリストに追加し、必要な場合は古いメッセージをパージし、更新されたメッセージリストを将来のインタラクションのためにセッション状態に保存します。

注：このコードは、Azure OpenAI ServiceとStreamlit用に特別に設計されています。これらのサービスの機能を活用して、シンプルなチャットボットインターフェースを作成します。

![chatbot-AZ_screen](https://github.com/potofo/chatbot-AZ/assets/138992835/06a0c3f6-ccf0-490e-88f4-fdf5cba2cae5)

## 必要条件

- Azure OpenAIサービス:
  - このプログラムを動作させるには、Azure OpenAIのエンドポイント、APIキー、APIバージョンが必要です。
  - キー発行には、従量制のAzure OpenAIサービスへの登録が必要です。
  
- openaiパッケージ (Ver 0.27.8):
  - このプログラムでは、`openai`パッケージを使用してOpenAI APIと対話しています。

- Streamlit:
  -  プログラムはStreamlitバージョン1.24.0以上を必要とし、`streamlit_chat`を使用します。

- python-dotenv:
  -  プログラムはpython-dotenvバージョン1.0.0以上を必要とし、環境変数を取得します。

## Azure OpenAIサービスでOpenAIキーを発行する
Azure OpenAIサービスでAPIを発行するプロセスは以下の通りです：

1. Azureポータルにログインします。
2. リソースグループを作成します。
3. リソースグループ内でAzure OpenAIサービスを作成します。
4. Azure OpenAI StudioでLLMをデプロイします。
5. Azure OpenAIサービスに戻って必要な情報を取得します（エンドポイント、APIキー、APIバージョン）。

Azure OpenAIサービスでAPIを発行するプロセスです。詳細な手順については、公式のAzureドキュメンテーションを参照してください。

## 作者
- potofo

## 改訂
- 2023/09/30 01-00 potofo: 初版作成。
- 2023/10/01 01-01 portfo: アシスタントからのインクリメンタルな応答を修正。
- 2023/10/06 01-02 portfo: Azure App Serviceと環境変数に対するパラメータ化を考慮。
- 2024/02/03 01-03 portfo: OPENAI_API_VERSIONを最新版に修正。

## 免責事項
このプログラムによって引き起こされるいかなる問題についても、私たちは責任を負いません。 

## 制限事項
-

## ライセンス
- MIT ライセンス

## 著作権
- Copyright (c) 2023 potofo. All rights reserved.

## 注意点
-