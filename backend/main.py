import os
from dotenv import load_dotenv
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import openai
from openai import OpenAI

# Load the environment variables from .env
load_dotenv()

# Set up default values for OpenAI client
client = OpenAI()

# Set up FastAPI settings
app = FastAPI()

# Allow CORS for local development (adjust origins as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("ORIGINS")],  # React app runs on port 3000
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    """OpenAI message model"""
    content: str

@app.post("/chat/", tags=["Chatbot"])
async def chat(message: Message):
    """OpenAI chat endpoint
    Args:
        message: User chat input
    
    Returns:
        OpenAI response
    """
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
