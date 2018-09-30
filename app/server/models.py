import datetime


class Post:

    def __init__(self, data):
        self.data = data
        self.path_csv = '../../client/static/temp.csv'

    @property
    def post_id(self):
        return self.data['id']

    @property
    def year(self):
        dt = self.data['date']
        return datetime.datetime.fromtimestamp(dt).year

    @property
    def week_day(self):
        dt = self.data['date']
        return datetime.datetime.fromtimestamp(dt).weekday()

    @property
    def month(self):
        dt = self.data['date']
        return datetime.datetime.fromtimestamp(dt).month

    @property
    def hour(self):
        dt = self.data['date']
        return datetime.datetime.fromtimestamp(dt).hour

    @property
    def text(self):
        return self.data['text']

    @property
    def att(self):
        attr_id = []
        try:
            for i in self.data['attachments']:
                i_type = i['type']
                if i_type == 'photos_list':
                    pass
                else:
                    attr_id.append(str(i[i_type]['id']))
            return ', '.join(attr_id)
        except KeyError:
            return ''

    @property
    def num_att(self):
        try:
            num = len(self.data['attachments'])
            for i in self.data['attachments']:
                i_type = i['type']
                if i_type == 'photos_list':
                    num -= 1
            return num
        except KeyError:
            return 0

    @property
    def num_likes(self):
        return self.data['likes']['count']

    @property
    def num_reposts(self):
        return self.data['reposts']['count']

    @property
    def num_comments(self):
        return self.data['comments']['count']
