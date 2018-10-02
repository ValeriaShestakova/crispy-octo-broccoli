from flask import (
    render_template, redirect, send_file, url_for, flash)
from app.server.main.functions import *
from app import app
from app.server.forms import EnterForm, CsvForm, StatisticForm


@app.route('/')
def index():
    form = EnterForm()
    return render_template('form.html', form=form)


@app.route('/enter_data', methods=['GET', 'POST'])
def enter_data():
    form = EnterForm(meta={'csrf': app.config['CSRF_ENABLED']})
    if form.validate_on_submit():
        enter_id = form.enter_id.data
        begin_date = form.begin_date.data
        if enter_id.isdigit():
            if form.type_id.data == 'group':
                enter_id = f'-{enter_id}'
            valid, error_mes = check_data_vk(enter_id, begin_date)
            if valid is True:
                return redirect(url_for('get_data', enter_id=enter_id,
                                        begin_date=str(begin_date)))
        else:
            error_mes = 'ID must be a number'
    else:
        error_mes = form.errors
    return render_template('form.html', form=form, error=error_mes)


@app.route('/get_data/<enter_id>&<begin_date>', methods=['GET', 'POST'])
def get_data(enter_id, begin_date):
    form_csv = CsvForm()
    form_statistic = StatisticForm(meta={'csrf': app.config['CSRF_ENABLED']})
    if form_csv.validate_on_submit():
        all_posts = get_data_posts(enter_id,  begin_date, form_csv.csv_param.data)
        to_csv(form_csv.csv_param.data, all_posts)
        path = app.config["PATH_DOWNLOAD_CSV"]
        return send_file(path, as_attachment=True,
                         attachment_filename='statistics.csv')
    return render_template('get_data_posts.html', enter_id=enter_id,
                           begin_date=begin_date,
                           form_csv=form_csv,
                           form_statistic=form_statistic)


@app.route('/get_statistic/<enter_id>&<begin_date>', methods=['GET', 'POST'])
def get_statistic(enter_id, begin_date):
    form_csv = CsvForm()
    form_statistic = StatisticForm(meta={'csrf': app.config['CSRF_ENABLED']})
    if form_statistic.validate_on_submit():
        type_measure = form_statistic.type_measure.data
        type_time = form_statistic.type_time.data
        y_count_posts, y_measure, x = \
            get_data_posts_measure(enter_id, begin_date, type_measure, type_time)
        legend_count = 'Number of posts'
        legend_avg = f'Average of {type_measure[4::]}'
        return render_template('graph.html', values_count=y_count_posts, labels=x,
                               legend_count=legend_count, values_avg=y_measure,
                               legend_avg=legend_avg, form_csv=form_csv,
                               form_statistic=form_statistic,
                               enter_id=enter_id, begin_date=begin_date)
    else:
        error_mes = 'Choose both parameters'
        flash(error_mes)
        return redirect((url_for('get_data', enter_id=enter_id,
                                 begin_date=begin_date)))
