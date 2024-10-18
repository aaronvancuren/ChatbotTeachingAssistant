"""Contains OpenAI API calls"""

import os
from openai import OpenAI, _exceptions
from fastapi import APIRouter, HTTPException
from backend.models.openai import *

client = OpenAI()
openai_router = APIRouter()

# Maintains a single conversation for a single user
conversation = []

@openai_router.post("/ask", tags=["Chatbot"])
async def chat(message: Message):
    """OpenAI chat endpoint for communciating with the specified OpenAI model
    Args:
        message: User chat input
    
    Returns:
        OpenAI response
    """
    try:
        # Adds the user input to the conversation
        conversation.append(message.content)
        
        # Sends the entire conversation to ChatGPT
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": conversation
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
        
        # Adds the ChatGPT response to the conversation
        conversation.append(reply)
        
        # Returns the ChatGPT response to the frontend to display
        return {"reply": reply}
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
