from faker import Faker
fake = Faker('en_GB')

from . import address


def example(name=None, surveyIds=[]):
    if name is None:
        name = fake.company()

    def gen_phone_number():
        def new():
            return fake.phone_number().replace('(', '').replace(')', '').replace(' ', '')
        pn = new()
        while(pn[0] == '+'):
            pn = new()
        return '+44' + pn[1:]

    definition = {
        'name': name,
        'surveys': surveyIds,
        'invoiceContact':
        {
            'name': fake.name(),
            'address': address.example(),
            'phoneNumber': gen_phone_number(),
            'email': fake.free_email()
        },
        'activePartner': fake.boolean(chance_of_getting_true=95)
    }

    return definition
