import openai
from django.conf import settings

openai.api_key = settings.OPENAI_API_KEY

def generate_questions(exam):
    prompt = f"""
    Create {exam.num_questions} multiple-choice questions for an exam on the topic of {exam.subject.name}. The questions should be suitable for elementary school students aged 7-12. Each question should have four answer choices, with one being the correct answer. The difficulty should match {exam.difficulty} and should align with the provided material.

    Material:
    {exam.material}

    For each question, provide:
    - A question text that is age-appropriate and easy to understand
    - Four answer choices, labeled A, B, C, D
    - Clearly indicate which option is the correct answer

    Format:
    Question 1: [Question text]
    A) [Answer choice A]
    B) [Answer choice B]
    C) [Answer choice C]
    D) [Answer choice D]
    Correct answer: [A/B/C/D]

    Question 2: [Question text]
    A) [Answer choice A]
    B) [Answer choice B]
    C) [Answer choice C]
    D) [Answer choice D]
    Correct answer: [A/B/C/D]

    ...
    """


    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # or another available model
        messages=[
            {"role": "system", "content": "You are an expert exam question creator."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1500,  # Adjust based on the number of questions and length
        temperature=0.7,
    )

    questions_text = response.choices[0].message['content'].strip()

    # Parse the response into individual questions
    questions = []
    for question_block in questions_text.split("\n\n"):
        lines = question_block.split("\n")
        if len(lines) >= 6:
            question_text = lines[0].replace("Question: ", "").strip()
            choices = {line[0]: line[3:].strip() for line in lines[1:5]}
            correct_answer = lines[5].replace("Correct answer: ", "").strip()
            questions.append({
                'text': question_text,
                'choices': choices,
                'correct_answer': correct_answer,
            })
    
    return questions
from .models import StudentAnswer
def evaluate_student_answers(student, exam):
    # Get all answers for the given student and exam
    student_answers = StudentAnswer.objects.filter(student=student, exam=exam)
    
    # Calculate the total number of questions and correct answers
    total_questions = student_answers.count()
    correct_answers = student_answers.filter(is_correct=True).count()
    
    # Calculate the numeric grade
    if total_questions > 0:
        numeric_grade = (correct_answers / total_questions) * exam.max_grade
    else:
        numeric_grade = 0

    # Gather incorrect answers and their details
    incorrect_answers = student_answers.filter(is_correct=False)
    incorrect_details = [
        {
            'question': answer.question.text,
            'correct_option': answer.question.correct_answer,
            'student_option': answer.selected_answer
        }
        for answer in incorrect_answers
    ]

    # Create a summary for AI
    performance_summary = (
        f"The student answered {correct_answers} out of {total_questions} questions correctly. "
        f"Here are the details of incorrect answers:\n"
        f" 'Question: {'question'}, Correct Answer: {'correct_option'}, Your Answer: {'student_option'}' for d in incorrect_details])\n\n"
        f"Provide constructive feedback to help the student improve based on these details."
    )

    # Generate feedback using OpenAI's chat model
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # or "gpt-3.5-turbo" if preferred
        messages=[
            {"role": "system", "content": "You are a helpful and constructive tutor."},
            {"role": "user", "content": performance_summary},
        ],
        max_tokens=300,
        temperature=0.7,
    )

    feedback = response.choices[0].message['content'].strip()

    return numeric_grade, feedback 