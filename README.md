
#### Initial Setup

uv sync

source ./venv/bin/activate

skyvern init

Would you like to run Skyvern locally or in the cloud? -> local

No local Postgres detected. Start a disposable container now? -> y

AI API Setup -> Novita or ollama

Do you want to enable an OpenAI-compatible provider? -> n

AI Model -> select 1, update .env -> NOVITA_LLAMA_3_3_70B

Browser type -> select 2(headful), update .env -> cdp-connect

skip analytics email

Would you like to configure the MCP server? -> n

skyvern run server
skyvern run ui(turn off)

./copy_api_key.sh

skyvern run ui

google-chrome-stable --remote-debugging-port=9222 --user-data-dir=/home/nroot/skyvern-profile