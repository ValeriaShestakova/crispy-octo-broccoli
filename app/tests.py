import unittest
from flask import url_for
from app import app


class TestCase(unittest.TestCase):
    def setUp(self):
        app.testing = True
        app.config['CSRF_ENABLED'] = False
        app.config['WTF_CSRF_METHODS'] = []
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_main_page(self):
        rv = self.app.get('/')
        assert b'Hello!' in rv.data

    def enter_data(self, enter_id, begin_date, type_id):
        return self.app.post('/enter_data', data=dict(
            enter_id=enter_id,
            begin_date=begin_date,
            type_id=type_id
        ), follow_redirects=True)

    def enter_param(self, enter_id, begin_date, csv_param):
        with app.test_request_context():
            url = url_for('get_data', enter_id=enter_id, begin_date=begin_date)
        return self.app.post(url, data=dict(
                csv_param=csv_param
            ), follow_redirects=True)

    def enter_statistic_param(self, enter_id, begin_date, type_time, type_measure):
        with app.test_request_context():
            url = url_for('get_statistic', enter_id=enter_id, begin_date=begin_date)
        return self.app.post(url, data=dict(
                type_measure=type_measure,
                type_time=type_time
            ), follow_redirects=True)

    def test_param(self):
        rv = self.enter_param('94372315', '01.02.2015',
        ['post_id, text,att, num_att, num_likes, num_reposts, num_comments'])
        assert b'Error' not in rv.data
        rv = self.enter_param('9437231', '01.02.2010',
        ['post_id, num_reposts, num_comments'])
        assert b'Error' not in rv.data
        assert b'Your entered data is correct' in rv.data

    def test_statistic_param(self):
        rv = self.enter_statistic_param('94372315', '2015-02-01', 'year',
                                        'num_reposts')
        assert b'Error' not in rv.data
        assert b'canvas' in rv.data

        rv = self.enter_statistic_param('9437231', '2015-02-01', 'year', '')
        assert b'Error' in rv.data
        rv = self.enter_statistic_param('9437231', '2015-02-01', '', 'num_likes')
        assert b'Error' in rv.data

    def test_enter_data(self):
        rv = self.enter_data('94372315', '01.02.2015', 'person')
        assert b'Your entered data is correct' in rv.data
        rv = self.enter_data('925', '20.03.2014', 'group')
        assert b'Your entered data is correct' in rv.data
        rv = self.enter_data('925', '506.03.2014', 'group')
        assert b'Error' in rv.data
        rv = self.enter_data('abc', '01.03.2014', 'group')
        assert b'Error' in rv.data
        rv = self.enter_data('123', '01.03.1003', 'group')
        assert b'Error' in rv.data
        rv = self.enter_data('123', 'abc', 'group')
        assert b'Error' in rv.data


if __name__ == '__main__':
    unittest.main()
