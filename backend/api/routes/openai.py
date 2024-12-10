"""Contains OpenAI API calls"""

import os
import json
import ast

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from openai import OpenAI, _exceptions
from pydantic import BaseModel
from typing import List, Dict, Tuple
from fastapi_msal.models import IDTokenClaims

from backend.database.chroma_database import nearest_neighbor_search, get_or_create_collection,initialize_chromadb

client = OpenAI()
openai_router = APIRouter()
chroma_client = initialize_chromadb()
collection = get_or_create_collection(chroma_client, 'file_collection')

initial_prompt = (
    "You are a helpful teaching assistant."
    "You should offer students guidance to help students understand the material. "
    "You should not provide students with direct solutions to problems. "
    "You should maintain a polite and supportive tone."
    "If you do not know the answer to a quetstion tell the student that you do not know and instruct them on where to find more information."
    "Only answer questions relevant to the course material."
    ""
                 )

class ChatRequest(BaseModel):
    user_content: str
    openai_model: str
    context: str

conversations: Dict[str,List[Tuple[str, str]]] = {}

@openai_router.post("/ask", tags=["Chatbot"])
async def chat(request: ChatRequest) -> str:
    """OpenAI chat endpoint for communciating with the specified OpenAI model
    Args:
        ChatRequest: contains the user's question, the OpenAI model to use, and the user context.

    Returns:
        List[Tuple[str,str]]: conversation updated with the response from OpenAI
    """
    try:
        claims: IDTokenClaims = IDTokenClaims.decode_id_token(ast.literal_eval(request.context)['id_token'])
        user_id = claims.user_id        
        conversation: List[Tuple[str, str]] = conversations.get(user_id, [])
        if not conversation:
            conversations.update({user_id: conversation})

        conversation.append({'role': 'system', 'content': initial_prompt})

        if not request.user_content.strip():
                raise HTTPException(status_code=400, detail="The input content cannot be empty.")

        # Moderation API Call
        try:
            moderation_response = client.moderations.create(
                model="omni-moderation-latest",
                input=request.user_content
            )
            print(moderation_response.results)
            if moderation_response.results and moderation_response.results[0].flagged:
                return JSONResponse(content={
                    "message": "Your input violates our content guidelines. Please modify your question and try again.",
                    "flagged_categories": moderation_response.results[0].categories
                })

        except (KeyError, IndexError, AttributeError) as e:
            raise HTTPException(status_code=500, detail=f"Moderation API returned an unexpected response: {str(e)}")

        except _exceptions.APIError as e:
            raise HTTPException(status_code=502, detail=f"Moderation API error: {str(e)}")
                
        conversation.append({'role': 'user', 'content': request.user_content})
        
        relevant_docs = nearest_neighbor_search(collection=collection,input_text=request.user_content, n_results=3)

        if relevant_docs:
            system_message = "Relevant information:\n"
            for idx, doc in enumerate(relevant_docs, 1):
                system_message += f"{idx}. {doc['content']}\n"
            conversation.append({'role': 'system', 'content': system_message})

        # Sends the entire conversation to ChatGPT
        response = client.chat.completions.create(
            messages=conversation,
            model=request.openai_model,
            max_completion_tokens=int(os.getenv("OPENAI_MAX_COMPLETION_TOKENS")),
            n=1,
            stop=None,
            temperature=0.7
        )

        # Adds the ChatGPT response to the conversation
        conversation.append({'role': 'assistant', 'content': response.choices[0].message.content.strip()})

        # Returns the conversation to the frontend to display
        return json.dumps(conversation)
    except _exceptions.APIConnectionError as e:
        print("The server could not be reached")
        return json.dumps({"error": "APIConnectionError", "message": str(e)})
    except _exceptions.RateLimitError as e:
        print("A 429 status code was received; we should back off a bit.")
        return json.dumps({"error": "RateLimitError", "message": str(e)})
    except _exceptions.APIStatusError as e:
        print("Another non-200-range status code was received")
        return json.dumps({"error": "APIStatusError", "status_code": e.status_code, "message": str(e.message)})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
