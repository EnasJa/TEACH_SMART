# TEACH_SMART# TEACH_SMART
In many schools, teachers face significant challenges in addressing the wide range of learning levels within a single classroom. "TEACH SMART" offers an innovative solution based on advanced AI technologies and data processing. Unlike traditional education systems that lack advanced AI capabilities, TEACH SMART enables early detection of learning difficulties and personalized adaptation of educational materials. The project automates test creation by topic and difficulty level, provides automatic feedback and corrections, tracks student progress with visual reports, and offers teachers interaction with a natural language understanding chatbot that aids in teaching and additional resources.
The "TEACH SMART" project supports both teachers and students. Here’s how:

Teachers: The project helps teachers by providing tools to automate test creation, track student progress, and offer personalized feedback. It also includes an AI-based chatbot that assists teachers with teaching materials and additional resources. This helps teachers manage the varying learning levels within a classroom more effectively and efficiently.

Students: The system supports students by identifying learning difficulties early on and providing personalized learning materials. It helps students receive timely feedback and guidance tailored to their progress, ensuring that their learning needs are met.

-This project was created with: -Python -Django -HTML -CSS

# Clone the repository
git clone https://github.com/EnasJa/TEACH_SMART.git


# Change directory
cd web

# Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows, use venv\Scripts\activate

# Install dependencies
1. Install Python
Download and install Python 3.11 from the official Python website.
2. Download and Open the Project
Clone or download the project from the repository to your local machine.
Navigate to the project directory in your terminal or command prompt.
3. Install Django and Other Dependencies
1.Install Django: 
 pip install Django==5.0.6
2.Install OpenAI and dotenv:
pip install openai==0.28.1
pip install python-dotenv==1.0.1
4. Migrate the Project:
python manage.py makemigrations
python manage.py migrate --run-syncdb
5. Run the Project:python manage.py runserver


License & copyright
© Enas Jaber, Asia Nbary, Rawan khateeb, Anfal Alnbbari.
This project was developed as part of the "Software Project Management" course at SCE College.