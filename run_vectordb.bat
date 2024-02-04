call "venv\Scripts\activate.bat"
SET CHROMA_SERVER_AUTH_CREDENTIALS=secret_credentials
SET CHROMA_SERVER_AUTH_CREDENTIALS_PROVIDER=chromadb.auth.token.TokenConfigServerAuthCredentialsProvider
REM SET CHROMA_SERVER_AUTH_TOKEN_TRANSPORT_HEADER=AUTHORIZATION
SET CHROMA_SERVER_AUTH_PROVIDER=chromadb.auth.token.TokenAuthServerProvider

REM In case of specify data folder
REM chroma run --path db --port 8080

REM In case of default data folder
REM Data store is chroma_data under folder 
chroma run --port 8080