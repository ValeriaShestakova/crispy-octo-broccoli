import datetime
import json
import requests
import csv
from app.server.models import Post
from app import app


CODE = """
var ITERS = 25;
var COUNT = 100;
var posts = []; 
var req_params = {
        "owner_id" : Args.id, 
        "offset" : 0,         
        "count"  : COUNT,
        "v" : "5.52"          
};
var i = 0;

while(i < ITERS) {
    req_params.offset = i*COUNT-(-ITERS*COUNT*Args.offset);    
    var items = API.wall.get(req_params).items;     
    if (items.length == 0) {
        return posts;
    }    
    posts.push(items); 
    i = i-(-1);
}
return posts;
"""


def check_data_vk(enter_id, begin_date):
    url = f'https://api.vk.com/method/wall.get?owner_id={enter_id}&count=1' \
          f'&v=5.52&access_token={app.config["ACCESS_TOKEN"]}'
    obj = json.loads(requests.get(url).content)
    if begin_date < datetime.date(1970, 1, 1):
        return False, 'Date is not valid'
    dt = datetime.datetime.strptime(str(begin_date), "%Y-%m-%d").timestamp()
    if obj['response']['count'] == 0:
        return False, "Person or group don't have any posts"
    try:
        obj['error']
    except KeyError:
        if obj['response']['items'][0]['date'] < int(dt):
            return False, "Write an earlier date"
        else:
            return True, ''
    return False, 'Data is not valid'


def get_data_posts(enter_id, begin_date, param):
    dt = datetime.datetime.strptime(begin_date, "%Y-%m-%d").timestamp()
    all_posts = []
    run = True
    offset = 0
    while run:
        url = f'https://api.vk.com/method/execute?code={CODE}&id={enter_id}' \
              f'&offset={offset}&v=5.52' \
              f'&access_token={app.config["ACCESS_TOKEN"]}'
        obj = json.loads(requests.get(url).content)
        posts = obj['response']
        for item in posts:
            for post in item:
                if post['date'] >= int(dt):
                    post = Post(post)
                    post_info = []
                    for p in param:
                        post_info.append(getattr(post, p))
                    all_posts.append(post_info)
            if len(item) < 100:
                run = False
        offset += 1
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
