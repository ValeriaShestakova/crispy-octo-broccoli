from flask import (
    render_template, redirect, send_file)
from app.server.main.functions import *
from app import app
from app.server.forms import EnterForm, CsvForm, StatisticForm


@app.route('/')
def index():
    form = EnterForm()
    return render_template('form.html', form=form, show_message=False)


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
    form_csv = CsvForm()
    form_statistic = StatisticForm()
    enter_id, begin_date = flash_message()
    if form_csv.validate_on_submit():
        all_posts = get_data_posts(enter_id,  begin_date, form_csv.csv_param.data)
        to_csv(form_csv.csv_param.data, all_posts)
        path = app.config["PATH_DOWNLOAD_CSV"]
        return send_file(path, as_attachment=True,
                         attachment_filename='statistics.csv')
    return render_template('get_data_posts.html', form_csv=form_csv,
                           form_statistic=form_statistic)


@app.route('/get_statistic', methods=['GET', 'POST'])
def get_statistic():
    enter_id, begin_date = flash_message()
    form_csv = CsvForm()
    form_statistic = StatisticForm()
    if form_statistic.validate_on_submit():
        type_measure = form_statistic.type_measure.data
        type_time = form_statistic.type_time.data
        x_count_posts, x_measure, y = \
            get_data_posts_measure(enter_id, begin_date, type_measure, type_time)
        legend_count = 'Number of posts'
        legend_avg = f'Average of {type_measure[4::]}'
        return render_template('graph.html', values_count=x_count_posts, labels=y,
                               legend_count=legend_count, values_avg=x_measure,
                               legend_avg=legend_avg, form_csv=form_csv,
                               form_statistic=form_statistic)
    else:
        error_mes = 'Choose both parameters'
        flash(error_mes, 'error')
        return redirect('/get_data')
