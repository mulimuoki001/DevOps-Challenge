# Fitness Classes Booking Application

This project is a **Fitness Classes Booking** system built using **Django** and **PostgreSQL**. It allows users to book fitness classes, manage schedules, and interact with the application through a user-friendly interface.

## Table of Contents

- [Requirements](#requirements)
- [Setup Instructions](#setup-instructions)
  - [Install Dependencies](#install-dependencies)
  - [Setting Up the Database](#setting-up-the-database)
  - [Running the Development Server](#running-the-development-server)
- [Running Tests](#running-tests)
- [Docker Setup](#docker-setup)
- [Deployment](#deployment)
- [Troubleshooting](#troubleshooting)

## Requirements

- Python 3.12+
- Django 5.1.7
- PostgreSQL
- Docker (for containerization, optional)

## Setup Instructions

Follow these steps to set up and run the app locally.

### 1. Clone the Repository

First, clone the repository to your local machine:

      git clone https://github.com/ALU-BSE/devops-challenge-mulimuoki001.git
      cd fitness_classes_booking




## 2. Set Up the Database

### Start PostgreSQL and log in as the 'postgres' user
    psql -U postgres

### Create a new database for the app
      CREATE DATABASE fitness_db;

### Exit PostgreSQL
    \q

### Optional: Update the database settings in `settings.py` (located in `fitness_classes_booking/settings.py`)

### Open `settings.py` in a text editor and ensure the database settings are as follows:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'fitness_db',
            'USER': 'postgres',
            'PASSWORD': 'your_password',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }

## 3. Install Dependencies
With the virtual environment activated, now it's time to install all the dependencies.
### Install the required dependencies for the project. To do this, run the following command:
    pip install -r requirements.txt

## 4. Set up the Virtual Environment
  Next, set up a virtual environment to manage the project's dependencies
  
  ### For Linux/macOS
              python3 -m venv venv

  ### For Windows
              python -m venv venv


  Activate the virtual environment

  ### For Linux/macOS
    source venv/bin/activate

  ### For Windows
    venv\Scripts\activate

## 5. Run migrations
Once the database is set up, run the migrations to create the necessary tables:

    python manage.py migrate
This will apply all the database migrations and create the required tables.

## 6. Create a Superuser(Optional)
If you need access to the Django admin panel, create a superuser:

          python manage.py createsuperuser

Follow the prompts to set up a username, email, and password.

## 7. Running the Development Server
To start the development server and run the application locally:

    python manage.py runserver
    
By default, the server will run at http://127.0.0.1:8000/, but since you are using a custom port (8087), you can also run it as:

    python manage.py runserver 0.0.0.0:8087

You should now be able to visit the application by navigating to http://localhost:8087 in your browser.

## 8. Running Tests
To run the tests, you can use the following command:

       python manage.py test
This will execute the test cases in your Django application.

##9. Docker Setup (Optional)
If you prefer to run the application using Docker, follow these steps to set up the Docker environment.

Build and start the containers using Docker Compose:

    docker-compose up --build
This will start the containers for PostgreSQL, Django, and other services defined in your docker-compose.yaml file.

## 10. Deployment
To deploy the application, follow these instructions:

Set up the server to run the application in a production environment.

Configure the necessary environment variables for production.

Use Docker to deploy the app or set it up manually with the steps mentioned above.

11. Troubleshooting
If you encounter issues during setup or while running the app, here are some common problems and solutions:

CSRF Token Issues:

  If you’re seeing a CSRF verification error, make sure that your browser accepts    cookies and that the CSRF_COOKIE_SECURE and CSRF_TRUSTED_ORIGINS settings are     correctly configured in settings.py.

  Database Connection Issues:

  Ensure that PostgreSQL is running and accessible.

  Double-check your database configuration in settings.py.

  Missing Dependencies:

  Ensure that all required Python packages are installed by running pip install -r requirements.txt within your virtual environment.


  
