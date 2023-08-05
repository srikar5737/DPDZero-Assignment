# Backend API and Frontend Setup

This repository contains the code for a simple backend API and frontend setup using Flask as the backend framework and HTML/CSS/JavaScript as the frontend.

# Framework
- Backend: Flask (Python)
- Frontend: HTML, CSS, JavaScript
## Database Schema
The backend uses an SQLite database to store user information and data. The database schema is as follows:

Table: users   
Columns:  username, email, password, full_name , age and gender

Table: data   
Columns: key (primary key), value


## Instructions to Run the Code

1. Make sure you have Python 3 installed on your system.
2. Clone this repository to your local machine:
3. Navigate to the project directory:
4. Create a virtual environment (optional but recommended):  
  `python3 -m venv venv `  
 ` venv\Scripts\activate  `
6. Install the required packages:   
   `pip install -r requirements.txt `  
7. Run the Flask development server:
 `python app.py`
8. Access the frontend in your web browser:

Open `http://127.0.0.1:5000/` in your web browser to access the home page.

For user registration, click on the "User Registration" button on the home page.

For user login, click on the "Generate Token" link on the home page.

After logging in, you will have access to the "Store Data", "Retrieve Data" ,"Edit Data" and "Delete Data"functionalities.
