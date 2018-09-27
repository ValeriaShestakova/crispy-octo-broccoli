import datetime
import json
import requests
from app import app


class QueryData:

    def __init__(self, enter_id, begin_date, valid=False):
        self.id = enter_id
        self.date = datetime.datetime.strptime(str(begin_date), "%Y-%m-%d")\
            .timestamp()
        self.access_token = app.config['ACCESS_TOKEN']
        if valid is False:
            self.valid = self.check_data_vk()
        else:
            self.valid = valid

    def check_data_vk(self):
        url = f'https://api.vk.com/method/wall.get?owner_id={self.id}&count=1' \
              f'&v=5.52&access_token={self.access_token}'
        obj = json.loads(requests.get(url).content)
        flag = False
        try:
            obj['error']
        except KeyError:
            flag = True
            if obj['response']['items'][0]['date'] < int(self.date):
                flag = False
        return flag
