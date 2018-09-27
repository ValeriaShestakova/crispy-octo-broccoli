from flask import (
    render_template, redirect, flash)
from app import app
from app.server.forms import EnterForm, CsvForm


@app.route('/')
def index():
    form = EnterForm()
    return render_template('form.html', form=form)


@app.route('/enter_data', methods=['GET', 'POST'])
def enter_data():
    form = EnterForm()
    if form.validate_on_submit():
        flash(f'ID = {str(form.enter_id.data)}, begin_date = '
              f'{str(form.begin_date.data)}')
        return redirect('/get_data')
    return render_template('form.html',
                           form=form, error=form.errors)


@app.route('/get_data', methods=['GET', 'POST'])
def get_data():
    form = CsvForm()
    if form.validate_on_submit():
        print(form.csv_param.data)
    else:
        print(form.errors)
    return render_template('get_data.html', form=form)
