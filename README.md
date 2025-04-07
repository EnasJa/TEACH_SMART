TEACH SMART
"TEACH SMART" is an innovative educational project that leverages advanced AI technologies and data processing to assist both teachers and students in managing a diverse range of learning levels within a classroom. The system automates exam creation based on topic and difficulty level, provides real-time feedback and corrections, tracks student progress through visual reports, and offers teachers an AI-powered chatbot to assist in lesson planning and finding additional resources.

How the System Works:
System Architecture:

Automated Exam Creation: The AI generates exams based on a given topic and difficulty level, customized to the material provided by the teacher.

Automated Feedback and Corrections: After students complete the exam, the system provides immediate feedback, including corrections and explanations for wrong answers.

Student Progress Tracking: The system tracks student performance over time, offering visual reports for teachers to monitor progress and identify areas needing attention.

Teacher Chatbot: A chatbot powered by AI assists teachers in lesson planning, finding teaching materials, and answering educational questions.
Technologies Used:
Python 3.11: The primary programming language used for the backend logic and algorithms.

Django: A framework for building the web application, handling the user interface, API requests, database management, and more.

SQLite3: A lightweight database used for storing project data (student progress, exam results, etc.).

OpenAI API: Utilized for generating exam questions, providing chatbot functionality, and analyzing student feedback through natural language processing.
System Components:
1. Backend (Python & Django):
The core of the system is built using Django, which manages URLs, page rendering, and the overall flow of the application.

Modules include:

Exam Module: Handles the automatic creation of questions based on supplied material, using the OpenAI API for question generation.

Progress Tracking Module: Stores student data, exam results, and generates visual progress reports.

Teacher Module: Provides the teacher with access to the AI chatbot for assistance in lesson planning, teaching resources, and solving educational problems.

2. Frontend (HTML, CSS):
The user interface (UI) is designed to be simple and user-friendly for both teachers and students.

For teachers, the interface presents visual data on student progress, exam results, and detailed reports.

For students, the interface allows access to exams, feedback, and personalized learning materials.

3. AI Integration (OpenAI):
Automatic Question Generation: OpenAI is used to create exam questions based on the text provided by the teacher. For example, a teacher can provide material on a specific topic (e.g., "History of Israel") and specify the difficulty level, and the system will generate questions based on that text.

Teacher Chatbot: The chatbot helps teachers by providing support for lesson planning, offering educational resources, and answering teaching-related questions.

4. Data Flow:
Teachers provide the teaching material and set the difficulty level for exams.

Students take the exams, and the system collects their data and generates feedback immediately.


The collected data is analyzed, and the chatbot provides suggestions for improvement and additional resources based on student performance.
Technical Challenges:
Optimizing Question Generation: One of the primary challenges was ensuring that the generated questions are diverse and sufficiently complex to match each student's learning level. We used machine learning algorithms to optimize the question generation process.

Integration with OpenAI: We carefully planned how to integrate OpenAI’s API while ensuring data privacy and security. All communications with the API are encrypted, and the data is processed locally before being sent to the system.

Personalization and Feedback: Tailoring the feedback for each student based on their progress was a key challenge. We built algorithms to analyze student answers and generate personalized feedback based on their individual needs.


How to Set Up the Project:
Follow these steps to set up TEACH SMART on your local machine:
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

# Integration with OpenAI
TEACH SMART uses the OpenAI API to:

Generate exam questions based on provided material, difficulty level, and student grade.
Provide a chatbot that teachers can use for lesson assistance, planning help, and finding teaching resources.
Analyze and improve feedback for students using natural language understanding.

Ensure you have your OpenAI API key set as an environment variable or in a .env file:

OPENAI_API_KEY=your_api_key_here

```

License & Copyright

© Enas Jaber, Anfal Alnbbari, Rawan Khateeb, Asia Nbary.

This project was developed as part of the "Software Project Management" course at SCE College.
