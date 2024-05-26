# To-Do List Application

A web-based To-Do List application built with Flask that allows users to register, log in, and manage their tasks. The app supports task prioritization, due dates, and dark mode.

## Features

- User registration and authentication
- Task creation, deletion, and viewing
- Task prioritization (High, Medium, Low)
- Due dates for tasks
- Dark mode toggle
- User-specific task lists

## Prerequisites

- Python 3.6+
- pip (Python package installer)

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/yourusername/todo-app.git
    cd todo-app
    ```

2. Create a virtual environment and activate it:

    ```sh
    python -m venv env
    source env/bin/activate # On Windows use `env\Scripts\activate`
    ```

3. Install the required packages:

    ```sh
    pip install -r requirements.txt
    ```

4. Create the instance folder:

    ```sh
    mkdir instance
    ```

5. Run the application:

    ```sh
    flask run
    ```

    The application will be available at `http://127.0.0.1:5000`.

## Usage

1. Open your browser and go to `http://127.0.0.1:5000`.
2. Register a new account or log in with an existing account.
3. Use the interface to add, view, and delete tasks.
4. Toggle dark mode using the link in the navigation bar.


## Dependencies

- Flask
- Flask-Login
- Flask-WTF
- WTForms
- Werkzeug

## Adding More Features

To enhance the application further, consider adding the following features:

- Task editing
- Task completion status
- User profile management
- Task sharing
- Integration with calendar applications

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -am 'Add your feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Create a new Pull Request



## Acknowledgments

- Flask Documentation
- Bootstrap for the front-end styling
- Flask-Login for managing user sessions

---
