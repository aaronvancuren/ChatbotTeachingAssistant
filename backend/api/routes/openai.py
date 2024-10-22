"""Contains OpenAI API calls"""

import os
from openai import OpenAI, _exceptions
from fastapi import APIRouter, HTTPException
from typing import List, Tuple

client = OpenAI()
openai_router = APIRouter()

@openai_router.post("/ask", tags=["Chatbot"])
async def chat(chatbot: List[Tuple[str, str]], user_input: str) -> List[Tuple[str, str]]:
    """OpenAI chat endpoint for communciating with the specified OpenAI model
    Args:
        message: User chat input
    
    Returns:
        OpenAI response
    """
    try:
        messages = []
        for input_text, response_text in chatbot:
            messages.append({'role': 'user', 'content': input_text})
            messages.append({'role': 'assistant', 'content': response_text})

        # Adds the user input to the conversation
        messages.append({'role': 'user', 'content': user_input})
        
        # Sends the entire conversation to ChatGPT
        response = client.chat.completions.create(
            messages=messages,
            model=os.getenv("OPENAI_MODEL"),
            max_completion_tokens=int(os.getenv("OPENAI_MAX_COMPLETION_TOKENS")),
            n=1,
            stop=None,
            temperature=0.7,
            # TODO add user field once user authentication is figured out
        )
        
        # Adds the user input and ChatGPT response to the conversation
        chatbot.append((user_input, response.choices[0].message.content.strip()))
        
        # Returns the conversation to the frontend to display
        return chatbot
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
