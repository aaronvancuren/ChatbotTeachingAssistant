"""Contains OpenAI API calls"""

import os
import json

from fastapi import APIRouter, HTTPException, Request
from openai import OpenAI, _exceptions
from pydantic import BaseModel
from typing import List, Dict

from backend.models.converstation import Conversation
from backend.api.routes.auth import msal_auth
from backend.database.database_user_conversations import DEMO_LIST

from backend.database.chroma_database import nearest_neighbor_search, get_or_create_collection,initialize_chromadb

client = OpenAI()
openai_router = APIRouter()
chroma_client = initialize_chromadb()
collection = get_or_create_collection(chroma_client, 'file_collection')

class ChatRequest(BaseModel, Request):
    user_content: str
    openai_model: str
    context: str
    currentConversation: str

conversations: Dict[str,List[Conversation]] = {}

@openai_router.post("/ask", tags=["Chatbot"])
async def chat(request: ChatRequest) -> str:
    """OpenAI chat endpoint for communciating with the specified OpenAI model
    Args:
        ChatRequest: contains the user's question, the OpenAI model to use, and the user context.

    Returns:
        str: conversation updated with the response from OpenAI as a JSON string
    """
    try:
        reqBody = json.loads(await request.body())

        user_session = await msal_auth.handler.get_token_from_session(request)
        user_id = user_session.id_token_claims.user_id

        if (not conversations.get(user_id, [])):    # For Testing
            conversations[user_id] = DEMO_LIST

        conversation: List[Conversation] = conversations.get(user_id, [])
        currentConversation: Conversation = next((convo for convo in conversation if str(convo.id) == reqBody['currentConversation']), Conversation())

        if not currentConversation:
            conversation.append(currentConversation)

        currentConversation.discussion.append({'role': 'user', 'content': reqBody['user_content']})

        relevant_docs = nearest_neighbor_search(collection=collection,input_text=reqBody['user_content'], n_results=3)

        if relevant_docs:
            system_message = "Relevant information:\n"
            for idx, doc in enumerate(relevant_docs, 1):
                system_message += f"{idx}. {doc['content']}\n"
            conversation.append({'role': 'system', 'content': system_message})

        # Sends the entire conversation to ChatGPT
        response = client.chat.completions.create(
            messages=currentConversation.discussion,
            model=reqBody['openai_model'],
            max_completion_tokens=int(os.getenv("OPENAI_MAX_COMPLETION_TOKENS")),
            n=1,
            stop=None,
            temperature=0.7
        )

        # Adds the ChatGPT response to the conversation
        currentConversation.discussion.append({'role': 'assistant', 'content': response.choices[0].message.content.strip()})

        # Returns the conversation to the frontend to display
        return json.dumps(currentConversation.discussion)
    except _exceptions.APIConnectionError as e:
        print("The server could not be reached")
        print(e.__cause__)  # an underlying Exception, likely raised within httpx.
    except _exceptions.RateLimitError as e:
        print("A 429 status code was received; we should back off a bit.")
        print(e.status_code)
    except _exceptions.APIStatusError as e:
        print("Another non-200-range status code was received")
        print(e.status_code)
        print(e.response)
        print(e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
