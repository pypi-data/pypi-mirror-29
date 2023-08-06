from faker import Faker
fake = Faker('en_GB')


def example(survey_ids, country=None):
    return {
        'name': fake.name(),
        'year': fake.year(),
        'country': fake.country() if country is None else country,
        'surveyType': fake.words(nb=1, ext_word_list=["domestic", "non-domestic", "transient"])[0],
        'surveys': survey_ids,
    }
