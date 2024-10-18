# Installation Guide

This guide will help you set up the Chatbot Teaching Assistant application using the OpenAI API with a FastAPI backend. You'll be using Visual Studio Code (VSCode) for development and Git Bash for running Python and pip commands.

## Prerequisites

- **Python 3.12+** installed. [Download Python](https://www.python.org/downloads/)
- **Git Bash** installed. [Download Git Bash](https://git-scm.com/downloads)
- **Visual Studio Code 1.93+** installed. [Download VSCode](https://code.visualstudio.com/download)
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

- **On Windows**:

```bash
py -m venv venv
```

- **On Unix or MacOS**:

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

Update pip to ensure latest version:

```bash
pip install --upgrade pip
```

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file from the `.env.template` file.

> The OpenAI environment variables can be found on the OpenAI Platform.

### 5. Run the FastAPI Server

Start the server using Uvicorn:

```bash
uvicorn main:app --reload
```

Alternatively, you can use run.py:
```bash
python run.py
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

### Setting Up Authentication
Using Microsoft Entra, find (our application)[https://entra.microsoft.com/#view/Microsoft_AAD_RegisteredApps/ApplicationMenuBlade/~/Overview/appId/973d0063-2640-4751-9edf-4a103b364b8f/isMSAApp~/false] and retrieve or create `client_id`, `tenant_id`, and `client_credential`. Set each of these in their corresponding environment variables in your `.env`.

- **Customizing Redirects**
  Ensure that all redirects are approved and included in the application under `Authentication`.
- **Customizing Permissions**
  Reference this (document)[] to ensure that the permissions you are requesting exist and are accessable.
  > [!NOTE]  
  > We do not have admin approval or permission with this app, therefore only permissions that don't require admin delegate privaleges should be used.

  > [!NOTE]  
  > For application permissions, the user must grant our application access to run as them and are unreliable.

## Dependencies

- `annotated-types`: Provides support for annotated type hints in Python.
- `anyio`: Asynchronous networking and concurrency library.
- `beautifulSoup4`: Handles reading HTML files.
- `certifi`: Mozilla’s curated collection of Root Certificates.
- `click`: Package for creating command-line interfaces.
- `colorama`: Produces colored terminal text on Windows.
- `dnspython`: DNS toolkit for Python.
- `email-validator`: Robust email address syntax and deliverability validator.
- `fastapi`: Web framework for building APIs.
- `fastapi-cli`: CLI tool to manage FastAPI projects.
- `fastapi_msal`: Out of the box support for microsoft MSAL authentication.
- `h11`: Pure-Python HTTP/1.1 protocol implementation.
- `h2`: Python HTTP/2 protocol implementation.
- `hpack`: HTTP/2 header encoding for Python.
- `httpcore`: Low-level HTTP client interface.
- `httptools`: HTTP parsing tools collection.
- `httpx`: Fully featured HTTP client supporting HTTP/1.1 and HTTP/2.
- `hyperframe`: Python module for working with HTTP/2 frames.
- `idna`: Implements Internationalized Domain Names in Applications (IDNA) standard.
- `identity`: Implements Microsoft Entra user authentication.
- `itsdangerous`: Securely signs data.
- `Jinja2`: Templating engine for generating HTML.
- `markdown-it-py`: Markdown parser with full CommonMark support.
- `MarkupSafe`: String handling library for safe HTML and XML rendering.
- `mdurl`: URL parsing for markdown.
- `openai`: Provides convenient access to the OpenAI REST API.
- `pydantic`: Data validation and settings management using Python type annotations.
- `pydantic-extra-types`: Extra types for Pydantic.
- `pydantic-settings`: Settings management library for Pydantic.
- `pydantic-core`: Core engine powering Pydantic.
- `pylint`: Checks for errors, enforces a coding standard, looks for code smells, and can make suggestions about how the code could be refactored.
- `PyPDF2`: Extracts text from PDFs.
- `Python-docx`:Extracts text from Word documents.
- `Python-pptx`:Extracts text from Power Points.
- `Pygments`: Syntax highlighter for code.
- `python-dotenv`: Reads key-value pairs from `.env` file and adds them to the environment.
- `Python-magic`: Identifies file types by content.
- `python-multipart`: Streaming multipart parser for Python.
- `PyYAML`: YAML parser and emitter for Python.
- `rich`: Library for rich text and beautiful formatting in the terminal.
- `shellingham`: Detects the current user’s shell.
- `sniffio`: Library to detect which async library is running.
- `starlette`: Lightweight ASGI framework/toolkit for building high-performance async services.
- `striprtf`: Extracts plain text from RTF files.
- `tiktoken`: tokenizes text and counts token use.
- `typer`: Library for building CLI applications, designed to be easy to use with FastAPI.
- `typing_extensions`: Backports new type hinting features.
- `uvicorn`: Lightning-fast ASGI server implementation.
- `watchfiles`: File watching library for Python.
- `websockets`: Library for building WebSocket servers and clients in Python.

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

- [annotated-types Documentation](https://pypi.org/project/annotated-types/)
- [anyio Documentation](https://anyio.readthedocs.io/en/stable/)
- [beautifulsoup4 Documentation](https://pypi.org/project/beautifulsoup4/#description)
- [certifi Documentation](https://pypi.org/project/certifi/)
- [click Documentation](https://click.palletsprojects.com/en/stable/)
- [colorama Documentation](https://pypi.org/project/colorama/)
- [dnspython Documentation](https://www.dnspython.org/)
- [email-validator Documentation](https://pypi.org/project/email-validator/)
- [fastapi Documentation](https://fastapi.tiangolo.com/)
- [fastapi-cli Documentation](https://pypi.org/project/fastapi-cli/)
- [fastapi_msal](https://github.com/dudil/fastapi_msal)
- [h11 Documentation](https://h11.readthedocs.io/en/stable/)
- [h2 Documentation](https://python-hyper.org/projects/h2/en/stable/)
- [hpack Documentation](https://pypi.org/project/hpack/)
- [httpcore Documentation](https://www.python-httpx.org/httpcore/)
- [httptools Documentation](https://pypi.org/project/httptools/)
- [httpx Documentation](https://www.python-httpx.org/)
- [hyperframe Documentation](https://pypi.org/project/hyperframe/)
- [idna Documentation](https://pypi.org/project/idna/)
- [identity Documentation](https://pypi.org/project/identity/)
- [itsdangerous Documentation](https://pypi.org/project/itsdangerous/)
- [Jinja2 Documentation](https://jinja.palletsprojects.com/en/stable/)
- [markdown-it-py Documentation](https://markdown-it-py.readthedocs.io/en/latest/)
- [MarkupSafe Documentation](https://pypi.org/project/MarkupSafe/)
- [mdurl Documentation](https://pypi.org/project/mdurl/)
- [openai Documentation](https://platform.openai.com/docs/overview)
- [pydantic Documentation](https://docs.pydantic.dev/)
- [pydantic-extra-types Documentation](https://pypi.org/project/pydantic-extra-types/)
- [pydantic-settings Documentation](https://pypi.org/project/pydantic-settings/)
- [pydantic-core Documentation](https://docs.pydantic.dev/latest/usage/types/pydantic_core/)
- [Pygments Documentation](https://pygments.org/docs/)
- [pylint](https://pylint.pycqa.org/en/latest/index.html)
- [PyPDF2 Documentation](https://pypi.org/project/PyPDF2/)
- [python-dotenv Documentation](https://pypi.org/project/python-dotenv/)
- [python-docx Documentation](https://pypi.org/project/python-docx/)
- [python-magic Documentation](https://pypi.org/project/python-magic/)
- [python-multipart Documentation](https://pypi.org/project/python-multipart/)
- [python-pptx Documentation](https://pypi.org/project/python-pptx/#description)
- [PyYAML Documentation](https://pyyaml.org/wiki/PyYAMLDocumentation)
- [rich Documentation](https://rich.readthedocs.io/en/stable/)
- [shellingham Documentation](https://pypi.org/project/shellingham/)
- [sniffio Documentation](https://pypi.org/project/sniffio/)
- [starlette Documentation](https://www.starlette.io/)
- [striprtf Documentation](https://pypi.org/project/striprtf/)
- [tiktoken Documentation](https://pypi.org/project/tiktoken/)
- [typer Documentation](https://typer.tiangolo.com/)
- [typing_extensions Documentation](https://pypi.org/project/typing-extensions/)
- [uvicorn Documentation](https://www.uvicorn.org/)
- [watchfiles Documentation](https://pypi.org/project/watchfiles/)
- [websockets Documentation](https://websockets.readthedocs.io/en/stable/)
