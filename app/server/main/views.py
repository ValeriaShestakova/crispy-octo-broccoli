from flask import (
    render_template, redirect, flash, get_flashed_messages)
import datetime
from app import app
from app.server.forms import EnterForm, CsvForm
from app.server.models import QueryData


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
        if begin_date < datetime.date(1970, 1, 1):
            query_data = QueryData(enter_id, begin_date, False)
        else:
            query_data = QueryData(enter_id, begin_date)
        if query_data.valid is True:
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
    subject_info = {category: message for category, message in received_data}
    query_data = \
        QueryData(subject_info['enter_id'], subject_info['begin_date'], True)
    if form.validate_on_submit():
        return redirect('/')
    flash(query_data.id, 'enter_id')
    flash(subject_info['begin_date'], 'begin_date')
    return render_template('get_data.html', form=form)
