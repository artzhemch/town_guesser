import json
import os
from flask import Flask, render_template, redirect, request

from map_loader import load_map
from geocoder import get_adress_info
from town_chooser import get_random_variants, choose_random_town


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/member')
def member():
    with open("templates/members.json", "rt", encoding="utf8") as f:
        members_list = json.loads(f.read())
    return render_template('member.html', members_list=members_list)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'GET':
        current_page = game_loop()
        return current_page

    elif request.method == 'POST':
        answer = request.form.get('chosen_town', '')
        current_page = game_loop()
        print(answer)
        return current_page


def game_loop():
    town = choose_random_town()
    load_map(town)
    params = {'image_source': os.path.join('static', 'img', 'tmp.png'),
              'text': get_adress_info(town),
              'variants': get_random_variants(town, n=3)}
    return render_template('map_page.html', **params)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
