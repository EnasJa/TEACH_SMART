# TEACH SMART

In many schools, teachers face significant challenges in addressing the wide range of learning levels within a single classroom. **"TEACH SMART"** offers an innovative solution based on advanced AI technologies and data processing. Unlike traditional education systems that lack advanced AI capabilities, TEACH SMART enables early detection of learning difficulties and personalized adaptation of educational materials. The project automates test creation by topic and difficulty level, provides automatic feedback and corrections, tracks student progress with visual reports, and offers teachers interaction with a natural language understanding chatbot that aids in teaching and additional resources. The "TEACH SMART" project supports both teachers and students. Here’s how:

## Teachers:
The project helps teachers by providing tools to automate test creation, track student progress, and offer personalized feedback. It also includes an AI-based chatbot that assists teachers with teaching materials and additional resources. This helps teachers manage the varying learning levels within a classroom more effectively and efficiently.

## Students:
The system supports students by identifying learning difficulties early on and providing personalized learning materials. It helps students receive timely feedback and guidance tailored to their progress, ensuring that their learning needs are met.

---

## Technologies Used:
- **Python**
- **Django**
- **SQLite3** (Database)
- **HTML**
- **CSS**

---
##
## How to Set Up

Follow these steps to set up the project on your local machine:

```bash
# Clone the repository
git clone https://github.com/EnasJa/TEACH_SMART.git

# Change directory
cd web

# Create a virtual environment (optional but recommended)
python -m venv venv

# Activate the virtual environment
# On Windows, use the following command:
# venv\Scripts\activate


# Install Python 3.11 (if not already installed)
# Download and install Python 3.11 from https://www.python.org/downloads/

# Install Django and other dependencies
pip install Django==5.0.6
pip install openai==0.28.1
pip install python-dotenv==1.0.1

# Migrate the Project (SQLite3 Setup)
# This project uses SQLite3 as the default database. Django automatically sets up SQLite3 for local development.
# Run the migration commands to set up the database:
python manage.py makemigrations
python manage.py migrate --run-syncdb

# Run the development server
python manage.py runserver
```
License & Copyright

© Enas Jaber, Anfal Alnbbari, Rawan Khateeb, Asia Nbary.

This project was developed as part of the "Software Project Management" course at SCE College.
