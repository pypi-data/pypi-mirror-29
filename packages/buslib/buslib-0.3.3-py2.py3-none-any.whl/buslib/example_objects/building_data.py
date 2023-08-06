from faker import Faker
from random import randint
fake = Faker('en_GB')


def example():
    return {
        'yearConstructed': fake.past_date(start_date="-100y", tzinfo=None).year,
        'grossInternalArea': '3000',
        'grossInternalAreaUnit': fake.words(nb=1, ext_word_list=['sqmeters', 'sqfeet'])[0],
        'storeys': randint(1, 20),
        'buildingType': fake.words(nb=1, ext_word_list=[
            'Commercial Office', 'Primary School', 'Secondary School', 'University Building',
            'Domestic Houses', 'Flats', 'Sheltered Housing', 'Student Acomomdation', 'Other'
        ])[0],
        'glazingType': fake.sentence(nb_words=3, variable_nb_words=True)[:-1],
        'glazingRatio': fake.words(nb=1, ext_word_list=['30%', '30%-50%',  '50%-70%', '>70%'])[0],
        'workStyle': fake.words(nb=1, ext_word_list=[
            'Open plan', 'Cellular', 'Hot desking', 'Other'
        ])[0],
        'displayEnergyCertificate': fake.words(nb=1, ext_word_list=[
            'A+', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'Unknown',
        ])[0],
        'energyPerformanceCertificate': fake.words(nb=1, ext_word_list=[
            'A+', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'Unknown',
        ])[0],
        'sustainabilityLabellingSchemes': fake.words(nb=randint(0, 3), ext_word_list=[
            'BREEAM', 'LEED', 'NABERS', 'GREEN STAR', 'WELL', 'Other'
        ]),
        'sustainabilityRatingsAchieved': fake.sentence(nb_words=4, variable_nb_words=True)[:-1],
        'ventilationType': fake.words(nb=1, ext_word_list=[
            'Natural','Mechanical','Mixed-Mode', 'Other'
        ])[0],
        'heatingType': fake.words(nb=1, ext_word_list=[
            'Radiators', 'All-air','Fan-coil units', 'Trench heating', 'Underfloor heating', 'Split-DX system', 'Other'
        ])[0],
        'coolingType': fake.words(nb=1, ext_word_list=[
            'None','Chilled beams', 'All-air', 'Fan-coil units', 'Split-DX system', 'Other'
        ])[0],
        'lightingType': fake.words(nb=1, ext_word_list=[
            'Fluorescent', 'LED', 'Halogen','Tungsten filament', 'Other', 'Unknown'
        ])[0],
        'windowControl': fake.words(nb=1, ext_word_list=[
            'Openable manual', 'Openable automatic', 'Not openable', 'Other'
        ])[0]
    }
