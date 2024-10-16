# Core Directory

The `core/` directory contains the core functionality and configurations essential for the application's operation. This includes global settings, template configurations, and other utility modules that are used throughout the project.

## **Contents**

- **`config.py`**: Defines the application settings using Pydantic's `BaseSettings`. It manages environment variables and configuration parameters.
- **`templates.py`**: Sets up Jinja2 templates for rendering HTML pages. It configures the templates directory and initializes the `Jinja2Templates` object.
- **`__init__.py`**: Initializes the `core` package.

## **Purpose**

- Centralizes configuration management.
- Provides utilities and core components that are reused across the application.
- Enhances maintainability by separating core functionalities from business logic.
