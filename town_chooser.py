import random
from data import db_session
from data.towns import Towns


all_variants = set()


def initiliaze_from_db():
    global all_variants
    db_session.global_init("db/town_guesser.sqlite")
    db_sess = db_session.create_session()
    all_towns = db_sess.query(Towns).all()
    all_variants = set(list(map(lambda town: town.town_name, all_towns)))


def get_random_variants(right_adress, n=3):
    """Возвращает n городов на выбор, один из которых верный"""
    global all_variants
    if not all_variants:
        initiliaze_from_db()
    return random.sample(all_variants - {right_adress}, n - 1) + [right_adress]


def random_town_generator():
    global all_variants
    shuffled_towns = list(all_variants)
    random.shuffle(shuffled_towns)
    for i in shuffled_towns:
        yield i


def choose_random_town(remake=False):
    """remake: загрузить снова БД"""
    global all_variants
    if not all_variants:
        initiliaze_from_db()
    try:
        x = random.choice(list(all_variants))
    except IndexError:
        print('База данных не найдена')
        raise IndexError
    return x
