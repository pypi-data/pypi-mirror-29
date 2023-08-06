from faker import Faker
fake = Faker('en_GB')


def example():
    return {
        'address_lines': fake.street_address().split('\n') + [fake.city()],
        'postcode': fake.postcode(),
        'country': 'UK'
    }
