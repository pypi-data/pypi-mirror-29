from faker import Faker
fake = Faker('en_GB')


def example(client=None, partner_id=None):
    def gen_phone_number():
        def new():
            return fake.phone_number().replace('(', '').replace(')', '').replace(' ', '')
        pn = new()
        while(pn[0] == '+'):
            pn = new()
        return '+44' + pn[1:]

    partner_id = partner_id if partner_id is not None else fake.words(nb=1, ext_word_list=[p['_id'] for p in client.partners.get()])[0]

    return {
        'email': fake.free_email(),
        'phoneNumber': gen_phone_number(),
        'name': fake.name(),
        'partner': partner_id
    }
