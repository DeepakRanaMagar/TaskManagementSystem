# Task Management System

Task Management System is a Django-based web application for managing tasks and sprints in a project management context.

***
## Features
<ul>
    <li>Create, Update and Delete Task</li>
    <li>Assign Tasks to Sprints</li>
    <li>Track Task Status</li>
    <li>View task details and associated sprint infromation</li>
</ul>

***
### Installation
To install and run the Task Management System, follow these steps:

1. Clone the repository:
    ```
    git clone git@github.com:DeepakRanaMagar/TaskManagementSystem.git
    ```

2. Navigate to the project directory:
    ```
    cd TaskManagementSystem
    ```

3. Create a virtual environment:
    ```
    python3 -m venv venv
    ```

4. Activate the virtual environment:
    - For Windows:
      ```
      venv\Scripts\activate
      ```
    - For macOS and Linux:
      ```
      source venv/bin/activate
      ```

5. Install the required dependencies:
    ```
    pip install -r requirements.txt
    ```

6. Apply the database migrations:
    ```
    python manage.py migrate
    ```

7. Start the development server:
    ```
    python manage.py runserver
    ```

8. Open your web browser and visit `http://localhost:8000` to access the Task Management System.

Note: Make sure you have Python and Django installed on your system before proceeding with the installation.

### Endpoints
Here are the available endpoints in this repository:

- `/tasks/`: List all tasks
- `/tasks/<task_id>/`: Retrieve a specific task
- `/sprints/`: List all sprints
- `/sprints/<sprint_id>/`: Retrieve a specific sprint
  
### API Documentation
The Task Management System provides API endpoints for interacting with tasks and sprints. You can refer to the Swagger API documentation integrated in this repository for detailed information on the available endpoints and their usage.

To access the Swagger API documentation, open your web browser and visit `http://localhost:8000/api/schema/swagger/` after starting the development server.

Note: The Swagger API documentation is automatically generated based on the API views and serializers defined in the Django project.

