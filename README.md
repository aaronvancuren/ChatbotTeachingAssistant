# Chatbot Teaching Assistant
The Chatbot Teaching Assistant is a tool for students and professors alike. It allows students to ask questions regarding enrolled course material including but not limited to lecures, homeworks, syllabi, related resources  without violating academic honesty. It allows professors to manage user access to courses and to provide course material to be used as context when answering student questions.

# Table of Contents
- [Installation Guide](#installation-guide)
- [How to Run](#how-to-run)
- [How to Use](#how-to-use)
- [How to Run Unit Tests](#how-to-run-unit-tests)
- [Credits](#credits)

# Installation Guide

This guide will help you set up the Chatbot Teaching Assistant application.

## Prerequisites

- [**Python 3.12**](https://www.python.org/downloads/release/python-3127/) installed.
- [**Docker**](https://docs.docker.com/desktop/setup/install/windows-install/) installed.
- [**Postgres 17+**](https://www.postgresql.org/download/) installed.

## Installation Steps

### 1. Clone the Repository

Open Git Bash or similar CLI and clone the repository:
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

When you're done, you can deactivate the virtual environment:

```bash
deactivate
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

Create a `.env` file from the `template.env` file.

Follow the below instructions for obtaining sensitive environment variables.

#### Microsoft Entra Environment Variables
- Go to [Microsoft Entra](https://entra.microsoft.com/#view/Microsoft_AAD_RegisteredApps/ApplicationMenuBlade/~/Credentials/appId/973d0063-2640-4751-9edf-4a103b364b8f)
- Click "New client secret"
- Update the "Description" to identify the secret
- Update the "Expires" as needed.

#### OpenAI Environment Variables
- Go to [OpenAI Platform](https://platform.openai.com/settings/organization/api-keys) to create an API key.
- Click "Create new secret key"
- Provide a "Name"
- Select Chatbot Teaching Assistant as the "Project"
- Click "Create secret key"

![OPENAI_API_KEY](README/OPENAI_API_KEY.png)

![client_credential](README/client_credential.png)

#### Session Management
- Run the following command to generate a secret key
  ```
  openssl rand -hex 32
  ```

### 5. Set Up PostgreSQL

#### Connect to the Cloud

##### Obtain SQL Instance Public IP Address
- Go to Google Cloud SQL
- Locate the 'chatbot-teaching-assistant-database' SQL Instance
- Obtain the Public IP Address

![Google Cloud SQL Instance](README/PostgresCloudStep1.png)
![Public IP Address](README/PostgresCloudStep2.png)

##### Add Personal IP Address to Authorize IP Addresses
- Click the Instance
- Go to the "connections" Section
- Go to the "Networking" Tab
- Click "Add a Network" and Enter IP Address

If you are adding an off-campus IP Address, delete the authorized IP Adress after use to limit security threats.

![Connections Tab](README/PostgresCloudStep3.png)
![Add IP Address](README/PostgresCloudStep4.png)

##### Connect Using pgAdmin 4 (PostgreSQL GUI)

- Register Server (name does not matter)
- Set Host Name (Public IP Address)
- Enter Username and Password

![Register Server](README/PostgresCloudStep5.png)
![Connection Details](README/PostgresCloudStep6.png)

#### Connect to Local Instance

##### Create Database Tables
- Start a Postgres Server (see Postgres documentation)
- Create a user named 'teaching-assistant' with CREATEDB permissions. (see Postgres documentation)

    note: this is dependency because the scripts were created for the cloud database which uses a teaching-assistant user.
- Run the 'create_tables.py' script found in the /scripts/database directory

Example:
```bash
python create_tables.py --host localhost --port 5432 --dbname chatbot --user teaching-assistant --password your-password
```

note: host, port, dbname, and user are optional as those are the default values.

# How to Run

Start the server using Uvicorn:

```bash
uvicorn backend.main:app --host [ENTER HOST] --port [ENTER PORT] --reload
```

Alternatively, you can use run.py:
```bash
python run.py
```

> The `--reload` flag enables auto-reloading of the server when code changes for development purposes only.

## Using Docker
Steps for using a dockerfile.

# How to Use

## Application
Create screenshots of using the application in the web.

## **Swagger UI** and **cURL**.

**Using Swagger UI:**

FastAPI automatically generates interactive API documentation using Swagger UI. You can access it by visiting:

- **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc UI:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

These interfaces allow you to interact with your API directly from the browser.

1. Go to the Swager UI or ReDoc UI in your browser.
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

# How to Run Unit Tests

The unittest module can be used from the command line to run tests:

...for modules
```bash
python -m unittest test_module1 test_module2
```

...for classes
```bash
python -m unittest test_module.TestClass
```

...for individual test methods
```bash
python -m unittest test_module.TestClass.test_method
```
# Setting up PostgreSQL Locally
Windows Install:

  Step 1: Download the Installer
    - Visit the official PostgreSQL download page: https://www.postgresql.org/download/windows/
    - Click on the "Download the installer" link, which will take you to the EnterpriseDB installer page.
    - Choose the version you want (e.g., PostgreSQL 16 is prefered for Google Cloud deployment) and download the appropriate installer for your system (32-bit or 64-bit).

  Step 2: Run the Installer
    - Locate the downloaded .exe file and double-click to run it.
    - If prompted by User Account Control (UAC), click "Yes" to allow the installer to make changes.

  Step 3: Follow the Installation Wizard

# Setting Up Google Cloud
- Go to [Google Cloud](https://console.cloud.google.com/)
- Create New Project
  - Select the current project in the upper left.
  - In the pop up, select "New Project"

    ![Create Google Project](README/CreateProjectStep1.png)

- Follow the prompts and click "CREATE"

  ![Confirm Google Project Creation](README/CreateProjectStep2.png)

- Go to Cloud Run
  1. Create Repository Service to Create Docker Image.

      ![Create Cloud Run Service](README/CreateCloudRunService.png)

    - Select "Continuously deploy from a repository (source or function)"
    - Click "SETUP WITH CLOUD BUILD"
    - Select a connected Repository
    - Click "NEXT"

      ![Continuous Deployment with Cloud Build](README/CloudRunServiceContinuousDeployment.png)

    - Select "Dockerfile" as the Build Type
    - Use the default Source location

      ![Build Configuration](README/CloudRunServiceBuildConfiguration.png)

  2. Create Container Service to Deploy Docker Image

      ![Create Cloud Run Service](README/CreateCloudRunService.png)

    - Select "Deploy one revision from an existing container image"
    - Click "SELECT" a Container image URL
    - Select the latest image created by the previous service
    - Click "Select"

      ![Deploy Container Image](README/CloudRunServiceDeployContainerImage.png)

    - Add Environment Variables and Secrets

      ![Add Environment Variables and Secrets](README/CloudRunServiceEnvironmentVariablesSecrets.png)

# Troubleshooting

- **Module Not Found Error:**
  - Ensure your virtual environment is activated and all dependencies are installed.

- **OpenAI Authentication Error:**
  - Verify that your OpenAI API key is correctly set in the `.env` file.

- **Server Not Running:**
  - Check if Uvicorn is installed and the correct app module is specified in the command.

- **Cannot Access Swagger UI:**
  - Ensure the server is running without errors and you're visiting the correct URL: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

# Credits
- [Aaron Van Curen](https://github.com/aaronvancuren) - Software Engineer (2024-2025)
- [Neal Birchfield](https://github.com/The-Architect01) - Software Engineer (2024-2025)
- [Wright Ceresa](https://github.com/wrightceresa) - Software Engineer (2024-2025)
- [Carter Besson](https://github.com/CarterBesson) - Software Engineer (2024-2025)
- [Dr. Zesheng Chen](https://users.pfw.edu/chenz/) - Academic Advisor/Project Cosponsor
- [Computer Science Department of Purdue Fort Wayne](https://www.pfw.edu/etcs/computer-science) - Project Cosponsor