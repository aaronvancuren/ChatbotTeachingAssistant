"""Contains OpenAI API calls"""

import os
import json
import ast

from fastapi import APIRouter, HTTPException
from openai import OpenAI, _exceptions
from pydantic import BaseModel
from typing import List, Dict, Tuple
from fastapi_msal.models import IDTokenClaims

import backend.database.database_user_conversations

client = OpenAI()
openai_router = APIRouter()

class ChatRequest(BaseModel):
    user_content: str
    openai_model: str
    context: str
    currentConversation: str

conversations: Dict[str,Dict[str,List[Tuple[str, str]]]] = {}

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
        conversation: Dict[str, List[Tuple[str, str]]] = conversations.get(user_id, [])
        currentConversation: List[Tuple[str, str]] = conversation.get(request.currentConversation, [])
        if not currentConversation:
            conversations.update({user_id: conversation})

        currentConversation.append({'role': 'user', 'content': request.user_content})
        
        # Sends the entire conversation to ChatGPT
        response = client.chat.completions.create(
            messages=currentConversation,
            model=request.openai_model,
            max_completion_tokens=int(os.getenv("OPENAI_MAX_COMPLETION_TOKENS")),
            n=1,
            stop=None,
            temperature=0.7
        )

        # Adds the ChatGPT response to the conversation
        currentConversation.append({'role': 'assistant', 'content': response.choices[0].message.content.strip()})

        next((convo 
              for convo in backend.database.database_user_conversations.DEMO_LIST(claims.user_id)
                if str(convo.id) == request.currentConversation), []).discussion = currentConversation

        # Returns the conversation to the frontend to display
        return json.dumps(conversation)
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
