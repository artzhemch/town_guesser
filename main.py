import json
import os
from flask import Flask, render_template, redirect, request, url_for

from map_loader import load_map
from geocoder import get_address_info
from town_chooser import get_random_variants, choose_random_town
from data import db_session
from data.add_town import AddTownForm
from data.towns import Towns
from data.fill_database import fill_database


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
score = 0
iteration_num = 0
NUMBER_OF_ROUNDS = 6
town_name = '_'


@app.route('/all_towns')
def all_towns():
    db_session.global_init("db/town_guesser.sqlite")
    db_sess = db_session.create_session()
    towns_list = db_sess.query(Towns.town_name).distinct().order_by(Towns.town_name)
    return render_template('all_towns.html', title='Все города', towns_list=towns_list)


@app.route('/', methods=['POST', 'GET'])
def index():
    global score, iteration_num, town_name

    if request.method == 'GET':
        town_name, current_page = game_loop()
        return current_page

    elif request.method == 'POST':
        iteration_num += 1
        answer = request.form.get('chosen_town', '')
        if answer == town_name:
            score += 1
        print(score, iteration_num)
        if iteration_num >= NUMBER_OF_ROUNDS:
            return redirect(url_for('scoreboard'))
        town_name, current_page = game_loop()
        return current_page


@app.route('/scoreboard')
def scoreboard():
    global score, iteration_num
    params = {'score': score,
              'back_href': '/',
              'max_score': NUMBER_OF_ROUNDS}
    print(params)
    page = render_template('score_page.html', title='Итоговый счёт', **params)
    iteration_num, score = 0, 0
    return page


@app.route('/addtown', methods=['GET', 'POST'])
def addtown():
    add_form = AddTownForm()
    if add_form.validate_on_submit():
        db_sess = db_session.create_session()
        town = Towns(
            town_name=add_form.town_name.data,
            api_request_string=add_form.api_request_string.data
        )
        db_sess.add(town)
        db_sess.commit()
        choose_random_town(remake=True)
        return redirect('/')
    return render_template('addtown.html', title='Добавляем город', form=add_form)


def game_loop():
    """Создаёт страницу для одного шага выбора. Возвращает её и верный ответ"""
    town = choose_random_town()
    print(town)
    load_map(town)
    params = {'image_source': os.path.join('static', 'img', 'tmp.png'),
              'text': get_address_info(town),
              'variants': get_random_variants(town, n=4)}
    return town, render_template('map_page.html', title='Town Guesser', **params)


if __name__ == '__main__':
    lost_database = True  # Флаг, что файл БД не найден
    if not os.path.isfile("db/town_guesser.sqlite"):
        lost_database = True
    db_session.global_init("db/town_guesser.sqlite")
    if lost_database:
        fill_database()
    app.run(port=8080, host='127.0.0.1')
