import copy
from faker import Faker
from random import randint
import stringcase
fake = Faker('en_GB')


def example(questionSets, group=None):

    title = fake.sentence(nb_words=5, variable_nb_words=True)[:-1]
    group = group if group is not None else fake.sentence(nb_words=2, variable_nb_words=True)[:-1]

    definition = {
        'name': stringcase.camelcase(stringcase.snakecase(title)),
        'type': fake.words(nb=1, ext_word_list=[
            'boolean',
            'shortText',
            'paragraph',
            'integer',
            'time',
            'date',
            'singleChoice',
            'multipleChoice',
            'leftHandScale',
            'rightHandScale',
            'centeredScale',
        ])[0],
        'group': group,
        'title': title,
        'questionSets': fake.words(nb=randint(1, len(questionSets)), ext_word_list=questionSets)
    }

    if definition['type'] == 'integer':
        definition['min'] = randint(0, 5)
        definition['max'] = randint(definition['min'] + 1, definition['min'] + 100)
    if definition['type'] == 'time':
        definition['min'] = randint(0, 100)
        definition['max'] = randint(definition['min'] + 30, definition['min'] + 120)
    if definition['type'] == 'singleChoice':
        definition['choices'] = {
            "%d" % (i+1): fake.sentence(nb_words=3, variable_nb_words=True)[:-1]
            for i in range(randint(3, 10))
        }
    if definition['type'] == 'multipleChoice':
        definition['choices'] = {
            "%d" % (i+1): fake.sentence(nb_words=3, variable_nb_words=True)[:-1]
            for i in range(randint(3, 10))
        }
    if definition['type'] == 'leftHandScale':
        definition['range'] = 7
        definition['minValue'] = fake.sentence(nb_words=2, variable_nb_words=True)[:-1]
        definition['maxValue'] = fake.sentence(nb_words=2, variable_nb_words=True)[:-1]
    if definition['type'] == 'rightHandScale':
        definition['range'] = 7
        definition['minValue'] = fake.sentence(nb_words=2, variable_nb_words=True)[:-1]
        definition['maxValue'] = fake.sentence(nb_words=2, variable_nb_words=True)[:-1]
    if definition['type'] == 'centeredScale':
        definition['range'] = 7
        definition['minValue'] = fake.sentence(nb_words=2, variable_nb_words=True)[:-1]
        definition['maxValue'] = fake.sentence(nb_words=2, variable_nb_words=True)[:-1]

    return definition
