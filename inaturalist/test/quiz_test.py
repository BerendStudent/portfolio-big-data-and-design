import random
import pandas




quiz_question_1 = {
    'question': 'What tree has a white trunk and tall leaves? ',
    'answer': 'Birch trees'
}

quiz_question_2 = {
    'question': 'What flower faces the sun? ',
    'answer': 'Sunflower'
}


questions = [quiz_question_1, quiz_question_2]


def get_question(questions):
    randomint = random.randint(0, len(questions))
    return questions[randomint]

question = get_question(questions)
response = input(question['question'])
if response == question['answer']:
    print('Hooray!')
else:
    print('Boo!')