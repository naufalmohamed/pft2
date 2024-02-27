# PFT

Welcome to PFT! This project is a simple Reddit-like application created using Flask, Python, and PostgreSQL.

## Features

- User authentication and authorization
- Posting and commenting on threads
- Upvoting and downvoting threads and comments
- Sorting threads by popularity, date, or number of comments
- User profiles with activity history

## Installation

To run this application locally, follow these steps:

1. Clone the repository: `git clone <repository-url>`
2. Navigate to the project directory: `cd <project-directory>`
3. Install dependencies: `pip install -r requirements.txt`
4. Set up PostgreSQL database:
   - Create a PostgreSQL database.
   - Update the database connection details in the `config.py` file.
   - Run database migrations: `flask db upgrade`

## Usage

Once you have completed the installation steps, you can start the Flask development server:

```bash
flask run
