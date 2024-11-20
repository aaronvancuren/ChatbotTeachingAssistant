"""Contains OpenAI API calls"""

import os
import json
import ast

from fastapi import APIRouter, HTTPException
from openai import OpenAI, _exceptions
from pydantic import BaseModel
from typing import List, Dict, Tuple
from fastapi_msal.models import IDTokenClaims

client = OpenAI()
openai_router = APIRouter()

class ChatRequest(BaseModel):
    user_content: str
    openai_model: str
    context: str

conversations: Dict[str,List[Tuple[str, str]]] = {}

@openai_router.post("/ask", tags=["Chatbot"])
async def chat(request: ChatRequest) -> str:
    """OpenAI chat endpoint for communciating with the specified OpenAI model
    Args:
        message: User chat input

    Returns:
        OpenAI response
    """
    try:
        claims: IDTokenClaims = IDTokenClaims.decode_id_token(ast.literal_eval(request.context)['id_token'])
        user_id = claims.user_id        
        conversation: List[Tuple[str, str]] = conversations.get(user_id, [])
        if not conversation:
            conversations.update({user_id: conversation})

        conversation.append({'role': 'user', 'content': request.user_content})
        
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
