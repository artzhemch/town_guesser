import json
import os
from flask import Flask, render_template, redirect, request, url_for

from map_loader import load_map
from geocoder import get_adress_info
from town_chooser import get_random_variants, choose_random_town


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
score = 0
iteration_num = 0
town = '_'


@app.route('/member')
def member():
    with open("templates/members.json", "rt", encoding="utf8") as f:
        members_list = json.loads(f.read())
    return render_template('member.html', members_list=members_list)


@app.route('/', methods=['POST', 'GET'])
def index():
    global score, iteration_num, town

    if request.method == 'GET':
        town, current_page = game_loop()
        return current_page

    elif request.method == 'POST':
        answer = request.form.get('chosen_town', '')
        if answer == town:
            score += 1
        print(score, iteration_num)
        if iteration_num >= 3:
            return redirect(url_for('scoreboard'))
        town, current_page = game_loop()
        return current_page


@app.route('/scoreboard')
def scoreboard():
    global score, iteration_num
    params = {'score': score,
              'back_href': '/'}
    print(params)
    page = render_template('score_page.html', **params)
    iteration_num, score = 0, 0
    return page


def game_loop():
    """Создаёт страницу для одного шага выбора. Возвращает её и верный ответ"""
    global iteration_num
    iteration_num += 1
    town = choose_random_town()
    load_map(town)
    params = {'image_source': os.path.join('static', 'img', 'tmp.png'),
              'text': get_adress_info(town),
              'variants': get_random_variants(town, n=3)}
    return town, render_template('map_page.html', **params)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
