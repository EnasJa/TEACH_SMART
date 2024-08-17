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
