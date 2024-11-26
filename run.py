"""Module provides an entry point to the application"""

import os
import uvicorn

from dotenv import load_dotenv

# Load the environment variables from .env
load_dotenv()

if __name__ == "__main__":
    uvicorn.run("backend.main:app",
                host=os.getenv("HOST"),
                port=int(os.getenv("PORT")),
                reload=True)
