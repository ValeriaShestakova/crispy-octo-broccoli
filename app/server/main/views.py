from flask import (
    render_template, redirect, flash, get_flashed_messages, send_file)
import datetime
import json
import requests
import csv
from app import app
from app.server.forms import EnterForm, CsvForm
from app.server.models import Post


def check_data_vk(enter_id, begin_date):
    url = f'https://api.vk.com/method/wall.get?owner_id={enter_id}&count=1' \
          f'&v=5.52&access_token={app.config["ACCESS_TOKEN"]}'
    obj = json.loads(requests.get(url).content)
    if begin_date < datetime.date(1970, 1, 1):
        return False
    dt = datetime.datetime.strptime(str(begin_date), "%Y-%m-%d").timestamp()
    try:
        obj['error']
    except KeyError:
        if obj['response']['items'][0]['date'] < int(dt):
            return False
        else:
            return True
    return False


def get_data_vk(enter_id, begin_date, param):
    url = f'https://api.vk.com/method/wall.get?owner_id={enter_id}' \
          f'&v=5.52&access_token={app.config["ACCESS_TOKEN"]}'
    obj = json.loads(requests.get(url).content)
    posts = obj['response']['items']
    dt = datetime.datetime.strptime(begin_date, "%Y-%m-%d").timestamp()
    all_posts = []
    for post in posts:
        if post['date'] >= int(dt):
            post = Post(post)
            post_info = []
            for p in param:
                post_info.append(getattr(post, p))
            all_posts.append(post_info)
    to_csv(param, all_posts)


def to_csv(param, all_posts):
    path = app.config["PATH_CSV"]
    with open(path, 'w', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(param)
        for p in all_posts:
            writer.writerow(p)


@app.route('/')
def index():
    form = EnterForm()
    return render_template('form.html', form=form)


@app.route('/enter_data', methods=['GET', 'POST'])
def enter_data():
    form = EnterForm()
    if form.validate_on_submit():
        enter_id = form.enter_id.data
        begin_date = form.begin_date.data
        if form.type_id.data == 'group':
            enter_id = (-1)*enter_id
        if check_data_vk(enter_id, begin_date) is True:
            flash(enter_id, 'enter_id')
            flash(str(begin_date), 'begin_date')
            return redirect('/get_data')
        else:
            error_mes = 'No such person or group, or date is not valid'
    else:
        error_mes = form.errors
    return render_template('form.html',
                           form=form, error=error_mes)


@app.route('/get_data', methods=['GET', 'POST'])
def get_data():
    form = CsvForm()
    received_data = get_flashed_messages(with_categories=True)
    mes_info = {category: message for category, message in received_data}
    flash(mes_info['enter_id'], 'enter_id')
    flash(mes_info['begin_date'], 'begin_date')
    if form.validate_on_submit():
        get_data_vk(mes_info['enter_id'],  mes_info['begin_date'], form.csv_param.data)
        path = app.config["PATH_DOWNLOAD_CSV"]
        return send_file(path, as_attachment=True,
                         attachment_filename='statistics.csv')
    return render_template('get_data.html', form=form)
