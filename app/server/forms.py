from flask_wtf import FlaskForm
from wtforms import DateField, IntegerField, SelectMultipleField, widgets
from wtforms.validators import DataRequired


class EnterForm(FlaskForm):
    enter_id = IntegerField('enter_id',  validators=[DataRequired()])
    begin_date = DateField('begin_date',  format='%d.%m.%Y')


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
