# Frontend Directory

The `frontend/` directory contains all the frontend assets of the application, including HTML templates and static files like CSS, JavaScript, and images. This directory is responsible for the client-side presentation and user interface of the application.

## **Contents**

- **`templates/`**: Holds Jinja2 HTML templates used for server-side rendering.
- **`static/`**: Contains static files served to the client, such as CSS stylesheets, JavaScript files, and images.

## **Purpose**

- **Templates**: Provide the structure and layout of the web pages. They allow the backend to render dynamic content by injecting data into the HTML before sending it to the client.
- **Static Files**: Enhance the user experience by adding styles, interactivity, and media to the web pages.

## **How It Works**

- The backend application uses the templates to render HTML pages by filling in dynamic content.
- Static files are served by the backend and linked within the templates using the `url_for('static', path='...')` function.

## **Development Tips**

- Keep the frontend assets organized to simplify maintenance and updates.
- Use template inheritance to reduce code duplication.
- Regularly update static files to improve performance and user experience.