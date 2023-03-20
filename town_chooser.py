import random


all_variants = {'Париж', 'Москва', 'Казань', 'Нью-Йорк'}


def get_random_variants(right_adress, n=3):
    """Возвращает n городов на выбор, один из которых верный"""
    return random.sample(all_variants - {right_adress}, n - 1) + [right_adress]


def random_town_generator():
    shuffled_towns = list(all_variants)
    random.shuffle(shuffled_towns)
    for i in shuffled_towns:
        yield i


def choose_random_town():
    global town_chooser
    try:
        x = next(town_chooser)
    except StopIteration:
        town_chooser = random_town_generator()
        x = next(town_chooser)
    return x


town_chooser = random_town_generator()
