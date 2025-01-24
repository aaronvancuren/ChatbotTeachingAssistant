"""Contains OpenAI API calls"""

import os
import json

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from openai import OpenAI, _exceptions
from pydantic import BaseModel
from typing import List, Dict
from backend.database.database_class_sections import get_user_classes
from backend.models.converstation import Conversation
from backend.api.routes.auth import msal_auth
from backend.database.database_user_conversations import DEMO_LIST

from backend.database.chroma_database import nearest_neighbor_search, get_or_create_collection,initialize_chromadb

client = OpenAI()
openai_router = APIRouter()
chroma_client = initialize_chromadb()
collection = get_or_create_collection(chroma_client, 'file_collection')


class ChatRequest(Request):
    user_content: str
    openai_model: str
    context: str
    currentConversationId: str

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
        reqBody = await request.json()

        user_session = await msal_auth.handler.get_token_from_session(request)
        user_id = user_session.id_token_claims.user_id

        if (not conversations.get(user_id, [])):    # For Testing
            conversations[user_id] = DEMO_LIST

        userConversation: List[Conversation] = conversations.get(user_id, [])
        currentConversation: Conversation = next((convo for convo in userConversation if str(convo.id) == reqBody['currentConversationId']), Conversation())


        currentConversation.discussion.append({'role': 'system', 'content': get_user_classes(user_id)[0].prompt})
    
        if not reqBody['user_content'].strip():
                raise HTTPException(status_code=400, detail="The input content cannot be empty.")

        # Moderation API Call
        try:
            moderation_response = client.moderations.create(
                model=os.getenv("OPENAI_MODERATIONS_MODEL"),
                input=reqBody['user_content']
            )

            if moderation_response.results and moderation_response.results[0].flagged:
                 # Adds the ChatGPT response to the conversation
                currentConversation.discussion.append({'role': 'assistant', 'content': "I can't answer that"})

                # Returns the conversation to the frontend to display
                return json.dumps(currentConversation.discussion)

        except (KeyError, IndexError, AttributeError) as e:
            raise HTTPException(status_code=500, detail=f"Moderation API returned an unexpected response: {str(e)}")

        except _exceptions.APIError as e:
            raise HTTPException(status_code=502, detail=f"Moderation API error: {str(e)}")
                
        currentConversation.discussion.append({'role': 'user', 'content': reqBody['user_content']})

        relevant_docs = nearest_neighbor_search(collection=collection,input_text=reqBody['user_content'], n_results=3)

        if relevant_docs:
            system_message = "Relevant information:\n"
            for idx, doc in enumerate(relevant_docs, 1):
                system_message += f"{idx}. {doc['content']}\n"
            currentConversation.discussion.append({'role': 'system', 'content': system_message})

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