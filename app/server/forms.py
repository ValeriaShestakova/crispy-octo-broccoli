from flask_wtf import FlaskForm
from wtforms import DateField, StringField, SelectMultipleField, widgets, RadioField
from wtforms.validators import DataRequired


class EnterForm(FlaskForm):

    enter_id = StringField('enter_id',  validators=[DataRequired()])
    begin_date = DateField('begin_date',  format='%d.%m.%Y')
    choices = [('person', 'person'),
               ('group', 'group')]
    type_id = RadioField(choices=choices)


class CsvParam(SelectMultipleField):

    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class CsvForm(FlaskForm):

    choices = [('post_id', 'post id'),
               ('text', 'text'),
               ('att', 'attachments'),
               ('num_att', 'number of attachments'),
               ('num_likes', 'number of likes'),
               ('num_reposts', 'number of reposts'),
               ('num_comments', 'number of comments')]
    csv_param = CsvParam('Label', choices=choices)


class StatisticForm(FlaskForm):

    choices_time = [('year', 'years'),
                    ('month', 'months'),
                    ('week_day', 'days of the week'),
                    ('hour', 'hours')]
    type_time = RadioField(choices=choices_time)
    choices_measure = [('num_likes', 'likes'),
                       ('num_reposts', 'reposts'),
                       ('num_comments', 'comments')]
    type_measure = RadioField(choices=choices_measure)
