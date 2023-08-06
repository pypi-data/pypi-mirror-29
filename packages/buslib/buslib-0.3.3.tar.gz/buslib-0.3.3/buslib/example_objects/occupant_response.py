from faker import Faker
from random import randint
import calendar
fake = Faker('en_GB')


def example(survey):

    def question_response(question):
        if question['type'] == 'boolean':
            return fake.boolean()
        if question['type'] == 'shortText':
            return fake.sentence(nb_words=10, variable_nb_words=True)
        if question['type'] == 'paragraph':
            return fake.paragraph(nb_sentences=3, variable_nb_sentences=True)
        if question['type'] == 'integer':
            return randint(question.get('min', 0), question.get('max', 100))
        if question['type'] == 'time':
            return randint(question.get('min', 0), question.get('max', 100))
        if question['type'] == 'date':
            return calendar.timegm(fake.date_between(start_date="-3y", end_date="today").timetuple())
        if question['type'] == 'singleChoice':
            return randint(1, len(question.get('choices').keys()))
        if question['type'] == 'multipleChoice':
            return [randint(1, len(question.get('choices').keys())) for i in range(randint(1, len(question.get('choices').keys())))]
        if question['type'] == 'leftHandScale':
            return randint(1, question.get('range', 7))
        if question['type'] == 'rightHandScale':
            return randint(1, question.get('range', 7))
        if question['type'] == 'centeredScale':
            return randint(1, question.get('range', 7))

    responses = map(lambda q: {'name': q['name'], 'response': question_response(q)}, survey['questions'])

    return {
        'survey': survey['_id'],
        'questions': list(responses)
    }
