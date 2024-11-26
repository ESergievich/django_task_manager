<div align="center">

<h1>Task Manager</h1>

<p>
A simple and flexible task management web application
</p>

[![Actions Status](https://github.com/ESergievich/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/ESergievich/python-project-52/actions)
[![.github/workflows/run_tests.yml](https://github.com/ESergievich/python-project-52/actions/workflows/run_tests.yml/badge.svg)](https://github.com/ESergievich/python-project-52/actions/workflows/run_tests.yml)
[![lint check](https://github.com/ESergievich/python-project-52/actions/workflows/lint_check.yml/badge.svg)](https://github.com/ESergievich/python-project-52/actions/workflows/lint_check.yml)
[![Maintainability](https://api.codeclimate.com/v1/badges/8fa283d0e884378e630a/maintainability)](https://codeclimate.com/github/ESergievich/python-project-52/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/8fa283d0e884378e630a/test_coverage)](https://codeclimate.com/github/ESergievich/python-project-52/test_coverage)

<p>

<a href="#about">About</a> •
<a href="#installation">Installation</a> •
<a href="#additionally">Additionally</a> 

</p>

</div>

## About

This task management web application is built using the Python Django framework. It allows users to create tasks, assign them to performers, and track their progress by changing task statuses. To access and interact with the system, users must first register and authenticate.

For a responsive, modern, and user-friendly interface, the project leverages the Bootstrap framework.

The frontend is rendered on the backend using DjangoTemplates. This approach means that the server generates the HTML, which is then sent to the client.

The application uses PostgreSQL as its object-relational database system.


### Features

* [x] Set tasks;
* [x] Assign performers;
* [x] Change task statuses;
* [x] Set multiple tasks labels;
* [x] Filter the tasks displayed;
* [x] User authentication and registration;

### Built With

* [Python](https://www.python.org/)
* [Django](https://www.djangoproject.com/)
* [Bootstrap 5](https://getbootstrap.com/)
* [PostgreSQL](https://www.postgresql.org/)
* [Poetry](https://python-poetry.org/)
* [Docker](https://www.docker.com/)
* [Flake8](https://flake8.pycqa.org/en/latest/)

### Details

For **_user_** authentication, the standard Django tools are used. In this project, users will be authorized for all actions, that is, everything is available to everyone.

Each task in the task manager usually has a **_status_**. With its help you can understand what is happening to the task, whether it is done or not. Tasks can be, for example, in the following statuses: _new, in progress, in testing, completed_.

**_Tasks_** are the main entity in any task manager. A task consists of a name and a description. Each task can have a person to whom it is assigned. It is assumed that this person performs the task. Also, each task has mandatory fields - author (set automatically when creating the task) and status.

**_Labels_** are a flexible alternative to categories. They allow you to group the tasks by different characteristics, such as bugs, features, and so on. Labels are related to the task of relating many to many.

When the tasks become numerous, it becomes difficult to navigate through them. For this purpose, a **_filtering mechanism_** has been implemented, which has the ability to filter tasks by status, performer, label presence, and has the ability to display tasks whose author is the current user.

---

## Installation


Clone the project:
```bash
>> git clone https://github.com/ESergievich/python-project-52.git && cd python-project-52
```

Create `.env` file in the root folder and add following variables:
```dotenv
DATABASE_URL=postgresql://postgres:password@db:5432/postgres
SECRET_KEY={your secret key} # Django will refuse to start if SECRET_KEY is not set
```

And run:
```shell
>> docker-compose up
```

The server is running at http://localhost:8000/

### Available Actions:

- **_Registration_** — First, you need to register in the application using the registration form provided;
- **_Authentication_** — To view the list of tasks and create new ones, you need to log in using the information from the registration form;
- **_Users_** — You can see the list of all registered users on the corresponding page. It is available without authorization. You can change or delete information only about yourself. If a user is the author or performer of a task, it cannot be deleted;
- **_Statuses_** — You can view, add, update, and delete task statuses if you are logged in. Statuses corresponding to any tasks cannot be deleted;
- **_Tasks_** — You can view, add, and update tasks if you are logged in. Only the task creator can delete tasks. You can also filter tasks on the corresponding page with specified statuses, performers, and labels;
- **_Labels_** — You can view, add, update, and delete task labels if you are logged in. Labels matching any tasks cannot be deleted.

---

## Additionally

### Dependencies

* python = "^3.10"
* django = "^5.0.7"
* django-bootstrap5 = "^24.2"
* django-filter = "^24.3"
* python-dotenv = "^1.0.1"
* dj-database-url = "^2.2.0"
* psycopg2-binary = "^2.9.9"
* gunicorn = "^22.0.0"
* django-extensions = "^3.2.3"

### Dev Dependencies

* flake8 = "^7.1.0"
* pytest-cov = "^5.0.0"
* pytest-django = "^4.8.0"
* coverage = "^7.6.8"
* codeclimate-test-reporter = "^0.2.3"

### Makefile Commands

<dl>
    <dt><code>make install</code></dt>
    <dd>Install all dependencies of the package.</dd>
    <dt><code>make migrate</code></dt>
    <dd>Generate and apply database migrations.</dd>
    <dt><code>make runserver</code></dt>
    <dd>Run Django development server at http://127.0.0.1:8000/</dd>
    <dt><code>make lint</code></dt>
    <dd>Check code with flake8 linter.</dd>
    <dt><code>make test</code></dt>
    <dd>Run tests.</dd>
    <dt><code>make check</code></dt>
    <dd>Validate structure of <code>pyproject.toml</code> file, check code with tests and linter.</dd>
    <dt><code>make shell</code></dt>
    <dd>Start Django shell (iPython REPL).</dd>
</dl>


This is the fourth and **final** training project of the ["Python Developer"](https://ru.hexlet.io/programs/python) course on [Hexlet.io](https://hexlet.io)
