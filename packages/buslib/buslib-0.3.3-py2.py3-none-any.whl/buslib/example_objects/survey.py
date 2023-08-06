from . import question, building_data, address
from faker import Faker
import calendar
from random import randint
from datetime import datetime
fake = Faker('en_GB')


def example(client, question_sets):
    question_set = fake.words(nb=1, ext_word_list=question_sets)[0]
    questions = client.questions.get(where={'questionSets': question_set})
    partner_ids = client.partners.get()
    return _example(partner_ids[randint(0, len(partner_ids)-1)], questions)


def example2(partner_ids, question_sets):
    return _example(partner_ids[randint(0, len(partner_ids)-1)], question_sets[randint(0, len(question_sets)-1)])


def _example(partner_id, questions):
    questions = [
        {key: q[key] for key in q.keys() if key[0] != "_" or key in ("_id", "_version")}
        for q in questions
    ]

    occupantCount = randint(50, 500)
    return {
        'createdBy': partner_id,
        'name': fake.sentence(nb_words=3, variable_nb_words=True),
        'buildingAddress': address.example(),
        'buildingData': building_data.example(),
        'surveyType': fake.words(nb=1, ext_word_list=["domestic", "non-domestic", "transient"])[0],
        'surveyMethod': fake.words(nb=1, ext_word_list=['paper', 'online', 'hybrid', 'other'])[0],
        'surveyDate': calendar.timegm(fake.date_between(start_date="-3y", end_date="today").timetuple()),
        'questions': questions,
        'occupantCount': occupantCount,
        'participantCount': randint(occupantCount//10, occupantCount)
    }
