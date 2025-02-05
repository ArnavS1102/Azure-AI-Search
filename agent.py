import os
import sys
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import FileSearchTool, MessageAttachment, FilePurpose
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()

ai_client = AIProjectClient.from_connection_string(
    credential=DefaultAzureCredential(), conn_str=os.getenv('PROJECT_CONNECTION_STRING')
)

if len(sys.argv) < 2:
    print("Usage: python3 agent1.py {QUESTION}")
    sys.exit(1)

user_question = sys.argv[1]

with ai_client:
    
    uploaded_doc = ai_client.agents.upload_file_and_poll(file_path='recipes.txt', purpose=FilePurpose.AGENTS)
    print(f"File uploaded successfully, ID: {uploaded_doc.id}")

    knowledge_base = ai_client.agents.create_vector_store_and_poll(file_ids=[uploaded_doc.id], name="vector_storage")
    print(f"Vector store created, ID: {knowledge_base.id}")

    document_search_tool = FileSearchTool(vector_store_ids=[knowledge_base.id])

    virtual_agent = ai_client.agents.create_agent(
        model="gpt-35-turbo",
        name="assistant_agent",
        instructions="You are an AI assistant that answers questions strictly based on search results",
        tools=document_search_tool.definitions,
        tool_resources=document_search_tool.resources,
    )
    print(f"AI Agent created, ID: {virtual_agent.id}")

    conversation_thread = ai_client.agents.create_thread()
    print(f"Thread initialized, ID: {conversation_thread.id}")

    user_query = ai_client.agents.create_message(
        thread_id=conversation_thread.id, role="user", content=user_question, attachments=[]
    )
    print(f"User message created, ID: {user_query.id}")

    assistant_response = ai_client.agents.create_and_process_run(thread_id=conversation_thread.id, assistant_id=virtual_agent.id)
    print(f"Processing run initiated, ID: {assistant_response.id}")

    ai_client.agents.delete_vector_store(knowledge_base.id)
    print("Vector store removed successfully")

    ai_client.agents.delete_agent(virtual_agent.id)
    print("AI Agent deleted")

    conversation_history = ai_client.agents.list_messages(thread_id=conversation_thread.id)

    chat_messages = conversation_history["data"]

    sorted_chat_messages = sorted(chat_messages, key=lambda x: x["created_at"])

    print("\n--- Conversation History (Sorted) ---")
    for chat in sorted_chat_messages:
        sender_role = chat["role"].upper()
        chat_content = chat.get("content", [])
        message_text = ""
        if chat_content and chat_content[0]["type"] == "text":
            message_text = chat_content[0]["text"]["value"]
        print(f"{sender_role}: {message_text}")
