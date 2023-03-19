import json
import os
from flask import Flask, render_template, redirect
from map_loader import load_map


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/member')
def member():
    with open("templates/members.json", "rt", encoding="utf8") as f:
        members_list = json.loads(f.read())
    return render_template('member.html', members_list=members_list)


@app.route('/')
def index():
    load_map('Париж')
    params = {'image_source': os.path.join('static', 'img', 'tmp.png')}
    return render_template('map_page.html', **params)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
