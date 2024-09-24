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
pip install "fastapi[standard]" uvicorn openai python-dotenv
```

Alternatively, if you have a `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Follow the instructions found in the template `env.txt` file in the `ChatbotTeachingAssistant/backend` directory:

Add your environment variables to the `env` file:

Rename the file to `.env`

### 5. Run the FastAPI Server

Start the server using Uvicorn:

```bash
uvicorn main:app --reload
```

> The `--reload` flag enables auto-reloading of the server when code changes.

### 6. Access the Swagger UI

FastAPI automatically generates interactive API documentation using Swagger UI. You can access it by visiting:

- **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc UI:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

These interfaces allow you to interact with your API directly from the browser.

### 7. Test the Chatbot

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

### 8. Open the Project in VSCode

Open the project directory in VSCode:

```bash
code .
```

Install the Python extension in VSCode for enhanced support.

### 9. Deactivate the Virtual Environment (Optional)

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

### Dependencies

- `fastapi`: Web framework for building APIs.
- `uvicorn`: ASGI server to run FastAPI.
- `openai`: OpenAI API client library.
- `python-dotenv`: Loads environment variables from a `.env` file.

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