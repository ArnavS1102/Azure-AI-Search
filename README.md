# AI Agent Script

## Overview
This script interacts with Azure AI services to create an AI agent capable of answering user queries based on uploaded documents. It performs the following steps:

1. Uploads a document to Azure AI.
2. Creates a vector store for retrieval-augmented generation (RAG).
3. Creates an AI agent using the GPT-35-Turbo model.
4. Initializes a conversation thread.
5. Processes the user’s question.
6. Retrieves and displays the conversation history.
7. Cleans up by deleting the vector store and AI agent.


## Setup


1. Install the required Python packages:
    ```sh
    pip install -r requirements.txt
    ```

3. Set up the environment variable:
    ```sh
    export PROJECT_CONNECTION_STRING="your_connection_string_here"
    ```
    Or add the following line to a `.env` file in the project directory:
    ```sh
    PROJECT_CONNECTION_STRING="your_connection_string_here"
    ```

## Running the Script
To run the script, pass your question as a parameter:

```sh
python3 agent1.py "Your question here"
