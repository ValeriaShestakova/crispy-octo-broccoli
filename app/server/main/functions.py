import datetime
import json
import requests
import csv
from app.server.models import Post
from app import app


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


def get_data_posts(enter_id, begin_date, param):
    # url = f'https://api.vk.com/method/wall.get?owner_id={enter_id}' \
    #       f'&offset=0&count = 1&extended = 0&v=5.52' \
    #       f'&access_token={app.config["ACCESS_TOKEN"]}'
    # count = json.loads(requests.get(url).content)
    # print(count)
    dt = datetime.datetime.strptime(begin_date, "%Y-%m-%d").timestamp()
    all_posts = []
    run = True
    offset = 0
    count = 100
    while run:
        url = f'https://api.vk.com/method/wall.get?owner_id={enter_id}' \
              f'&v=5.52&count={count}&offset={offset}' \
              f'&access_token={app.config["ACCESS_TOKEN"]}'
        obj = json.loads(requests.get(url).content)
        posts = obj['response']['items']
        for post in posts:
            if post['date'] >= int(dt):
                post = Post(post)
                post_info = []
                for p in param:
                    post_info.append(getattr(post, p))
                all_posts.append(post_info)
        if len(posts) < count:
            run = False
        offset += 100
    return all_posts


def to_csv(param, all_posts):
    path = app.config["PATH_CSV"]
    with open(path, 'w', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(param)
        for p in all_posts:
            writer.writerow(p)


def get_data_posts_measure(enter_id, begin_date, type_measure, type_time):
    param = (type_time, type_measure)
    all_posts = get_data_posts(enter_id, begin_date, param)
    x_count_posts = []
    x_measure = []
    y = []
    if type_time == 'year':
        begin_year = datetime.datetime.strptime(begin_date, "%Y-%m-%d").year
        current_year = datetime.datetime.now().year
        y = [i for i in range(begin_year, current_year+1)]
        x_count_posts, x_measure = get_avg_count(all_posts, y)
    elif type_time == 'month':
        y = [i for i in range(1, 13)]
        x_count_posts, x_measure = get_avg_count(all_posts, y)
    elif type_time == 'week_day':
        y = [i for i in range(0, 7)]
        x_count_posts, x_measure = get_avg_count(all_posts, y)
    elif type_time == 'hour':
        y = [i for i in range(0, 25)]
        x_count_posts, x_measure = get_avg_count(all_posts, y)
    return x_count_posts, x_measure, y


def get_avg_count(posts, time):
    x_count_posts = []
    x_measure = []
    for t in time:
        count_posts = 0
        count_measure = 0
        for p in posts:
            if p[0] == t:
                count_posts += 1
                count_measure += p[1]
        x_count_posts.append(count_posts)
        try:
            x_measure.append(count_measure/count_posts)
        except ZeroDivisionError:
            x_measure.append(0)
    return x_count_posts, x_measure
