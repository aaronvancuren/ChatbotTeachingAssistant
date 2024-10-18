# API Directory

The `api/` directory contains the application's routing logic, including both web routes for rendering HTML pages and API endpoints for handling JSON responses. It organizes the route definitions and any dependencies required by the routes.

## **Contents**

- **`routes/`**: A subdirectory that holds individual route modules.
  - **`openai.py`**: Contains OpenAI API calls.
  - **`web.py`**: Contains routes for rendering Jinja2 templates (server-side rendered web pages).
  - **`__init__.py`**: Initializes the `routes` package.
- **`dependencies.py`**: Defines dependencies that can be injected into route handlers, such as database sessions or authentication classes.
- **`__init__.py`**: Initializes the `api` package.

## **Purpose**

- Organizes all the route handlers in a modular fashion.
- Separates web page routes from API endpoints for clarity.
- Manages dependencies and middleware specific to the API layer.