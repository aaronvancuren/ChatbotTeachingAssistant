"""TODO: update docstring"""

import os
import openai
from openai import OpenAI
from fastapi import APIRouter, HTTPException
from backend.models.openai import *
from backend.database.base import *

openai_router = APIRouter()

# Set up default values for OpenAI client
client = OpenAI()

@openai_router.post("/ask", tags=["Chatbot"])
async def chat(user_id: int, conversation_id:int, message: Message):
    """OpenAI chat endpoint
    Args:
        message: User chat input
    
    Returns:
        OpenAI response
    """
    
    save_message(1, 1, "", message)
    conversation = get_conversation(1, 1)
    if not conversation:
        save
    
    try:
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": message.content
                }
            ],
            model=os.getenv("OPENAI_MODEL"),
            max_completion_tokens=int(os.getenv("OPENAI_MAX_COMPLETION_TOKENS")),
            n=1,
            stop=None,
            temperature=0.7,
            # TODO add user field once user authentication is figured out
        )
        reply = response.choices[0].message.content.strip()
        
        save_message(1, 1, "", reply)
        
        return {"reply": reply}
    except openai.APIConnectionError as e:
        print("The server could not be reached")
        print(e.__cause__)  # an underlying Exception, likely raised within httpx.
    except openai.RateLimitError as e:
        print("A 429 status code was received; we should back off a bit.")
        print(e.status_code)
    except openai.APIStatusError as e:
        print("Another non-200-range status code was received")
        print(e.status_code)
        print(e.response)
        print(e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
