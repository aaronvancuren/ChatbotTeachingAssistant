# Installation Guide

This guide will help you set up the Chatbot Teaching Assistant application using the OpenAI API with a FastAPI backend. You'll be using Visual Studio Code (VSCode) for development and Git Bash for running Python and pip commands.

## Prerequisites

- **Python 3.7+** installed. [Download Python](https://www.python.org/downloads/)
- **Git Bash** installed. [Download Git Bash](https://git-scm.com/downloads)
- **Visual Studio Code** installed. [Download VSCode](https://code.visualstudio.com/download)
- An **OpenAI API key**. [Sign up for OpenAI API](https://platform.openai.com/signup)

## Installation Steps

### 1. Clone the Repository

Open Git Bash and clone the repository:

```bash
git clone https://github.com/aaronvancuren/ChatbotTeachingAssistant.git
cd ChatbotTeachingAssistant
```

### 2. Create a Virtual Environment

Create a virtual environment to manage project dependencies:

```bash
python -m venv venv
```

Activate the virtual environment:

- **On Windows**:

  ```bash
  source venv/Scripts/activate
  ```

- **On Unix or MacOS**:

  ```bash
  source venv/bin/activate
  ```

### 3. Install Dependencies

Navigate to the `backend` directory:

```bash
cd backend
```

Install the required Python packages:

```bash
pip install fastapi uvicorn openai python-dotenv
```

Alternatively, if you have a `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the `ChatbotTeachingAssistant/backend` directory:

```bash
touch .env
```

Add your OpenAI API key to the `.env` file:

```env
OPENAI_API_KEY=your-openai-api-key
```

> **Note:** Replace `your-openai-api-key` with your actual OpenAI API key.

### 5. Create the FastAPI Application

Ensure that you have a `main.py` file in the `backend` directory with the following code:

```python
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI(
    title="Chatbot Teaching Assistant API",
    description="An API for a chatbot using OpenAI's GPT models",
    version="1.0.0"
)

class Prompt(BaseModel):
    prompt: str

@app.post("/chat", tags=["Chatbot"])
async def chat(prompt: Prompt):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt.prompt,
            max_tokens=150
        )
        return {"response": response.choices[0].text.strip()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### 6. Run the FastAPI Server

Start the server using Uvicorn:

```bash
uvicorn main:app --reload
```

> The `--reload` flag enables auto-reloading of the server when code changes.

### 7. Access the Swagger UI

FastAPI automatically generates interactive API documentation using Swagger UI. You can access it by visiting:

- **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc UI:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

These interfaces allow you to interact with your API directly from the browser.

### 8. Test the Chatbot

You can test the API endpoint using **Swagger UI**, **cURL**, or tools like **Postman**.

**Using Swagger UI:**

1. Go to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) in your browser.
2. Find the `/chat` POST endpoint.
3. Click on "Try it out".
4. Enter a prompt in the JSON body, for example:

   ```json
   {
     "prompt": "Hello, how are you?"
   }
   ```

5. Click "Execute" to see the response from the API.

**Using cURL:**

```bash
curl -X POST "http://127.0.0.1:8000/chat" -H "Content-Type: application/json" -d "{\"prompt\": \"Hello, how are you?\"}"
```

### 9. Open the Project in VSCode

Open the project directory in VSCode:

```bash
code .
```

Install the Python extension in VSCode for enhanced support.

### 10. Deactivate the Virtual Environment (Optional)

When you're done, you can deactivate the virtual environment:

```bash
deactivate
```

## Additional Information

### Setting Up Swagger with FastAPI

FastAPI comes with built-in support for interactive API documentation powered by **Swagger UI** and **ReDoc**. Here's how you can customize and utilize these features:

- **Customizing API Metadata:**

  You can set the title, description, and version of your API in the `FastAPI` instance:

  ```python
  app = FastAPI(
      title="Chatbot Teaching Assistant API",
      description="An API for a chatbot using OpenAI's GPT models",
      version="1.0.0"
  )
  ```

- **Disabling Docs:**

  If you want to disable the automatic documentation:

  ```python
  app = FastAPI(docs_url=None, redoc_url=None)
  ```

- **Custom Docs URLs:**

  You can set custom URLs for the documentation:

  ```python
  app = FastAPI(
      docs_url="/documentation",
      redoc_url="/redocs"
  )
  ```

- **Adding Tags to Routes:**

  You can organize your endpoints using tags:

  ```python
  @app.post("/chat", tags=["Chatbot"])
  async def chat(prompt: Prompt):
      # Your code here
  ```

### Dependencies

- `fastapi`: Web framework for building APIs.
- `uvicorn`: ASGI server to run FastAPI.
- `openai`: OpenAI API client library.
- `python-dotenv`: Loads environment variables from a `.env` file.

### Security Tip

- Never commit your `.env` file or API keys to version control.

### Git Bash Usage

- Git Bash emulates a Unix shell, allowing you to run shell scripts and commands on Windows.

## Troubleshooting

- **Module Not Found Error:**
  - Ensure your virtual environment is activated and all dependencies are installed.

- **OpenAI Authentication Error:**
  - Verify that your OpenAI API key is correctly set in the `.env` file.

- **Server Not Running:**
  - Check if Uvicorn is installed and the correct app module is specified in the command.

- **Cannot Access Swagger UI:**
  - Ensure the server is running without errors and you're visiting the correct URL: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Useful Links

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference/introduction)
- [Uvicorn Documentation](https://www.uvicorn.org/)
- [Python-dotenv Documentation](https://python-dotenv.readthedocs.io/en/latest/)
- [Swagger UI Documentation](https://swagger.io/tools/swagger-ui/)

---

I've corrected the links for the **FastAPI Documentation**, **Python-dotenv Documentation**, and **Swagger UI Documentation**:

- **FastAPI Documentation** now points to [https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/).
- **Python-dotenv Documentation** now points to [https://python-dotenv.readthedocs.io/en/latest/](https://python-dotenv.readthedocs.io/en/latest/).
- **Swagger UI Documentation** now points to [https://swagger.io/tools/swagger-ui/](https://swagger.io/tools/swagger-ui/).

The entire installation guide is written in markdown format so you can easily copy and paste it into your GitHub README.

Let me know if you need any further assistance!