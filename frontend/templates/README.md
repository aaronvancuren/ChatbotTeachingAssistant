# Templates Directory

The `templates/` directory contains Jinja2 HTML templates used by the application to render dynamic web pages. Templates are a powerful way to generate HTML with dynamic content, leveraging the flexibility of Jinja2 templating.

## **Contents**

- **`base.html`**: The base template that defines the common structure of your web pages (e.g., header, footer, navigation).
- **`index.html`**: Template for the home page, extending `base.html`.

## **Purpose**

- **Template Inheritance**: Allows child templates to inherit from a base template, promoting DRY (Don't Repeat Yourself) principles.
- **Dynamic Content Rendering**: Enables the backend to pass variables and data to the templates for rendering on the client side.

## **How It Works**

- Templates use Jinja2 syntax to include variables and control structures.
  - **Variables**: `{{ variable_name }}`
  - **Blocks**: `{% block content %}{% endblock %}`
- The backend renders these templates by providing context data, which populates the variables and controls the rendering logic.

## **Development Tips**

- **Organize Templates**: For larger projects, consider organizing templates into subdirectories.
- **Use Blocks Wisely**: Define blocks in `base.html` that child templates can override.
- **Avoid Logic in Templates**: Keep complex logic in the backend; templates should focus on presentation.