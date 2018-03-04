from flask import Flask, flash, render_template, request, redirect, jsonify, url_for, json
from flask_restful import Api, Resource, abort
import requests

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def homepage():
    return render_template('home.html')


@app.route('/task_summary')
def task_summary():
    task_list = requests.get('http://127.0.0.1:5000/tasks')
    # If there are no tasks, return no data
    if not task_list.json():
        return render_template('test.html')
    else:
        return render_template('test.html', table=task_list.json())


@app.route('/task_detail')
def task_detail():
    task_list = requests.get('http://127.0.0.1:5000/tasks')
    # If there are no tasks, return no data
    if not task_list.json():
        return render_template('test.html')
    # If there is one task, gather the details and return the data
    elif len(task_list.json()) == 1:
        detail = requests.get('http://127.0.0.1:5000/tasks/%s'%task_list.json()[0]['id'])
        return render_template('test.html', table2=detail.json())
    # If there are multiple tasks, iterate through each task
    else:
        detail = []
        for task in task_list.json():
            row = task['id']
            # Extend list
            detail.extend(requests.get('http://127.0.0.1:5000/tasks/%s'%row).json())
        return render_template('test.html', table2=detail)

@app.route('/status')
def status_page():
    task_list = requests.get('http://127.0.0.1:5000/tasks')
    # If there are no tasks, return no data
    if not task_list.json():
        return render_template('status.html')
    # If there is one task, gather the details and return the data
    elif len(task_list.json()) == 1:
        detail = requests.get('http://127.0.0.1:5000/tasks/%s'%task_list.json()[0]['id'])
        return render_template('status.html', table=detail.json())
    # If there are multiple tasks, iterate through each task
    else:
        detail = []
        for task in task_list.json():
            row = task['id']
            # Extend list
            detail.extend(requests.get('http://127.0.0.1:5000/tasks/%s'%row).json())
        return render_template('status.html', table=detail)


if __name__ == '__main__':
    app.run(debug=True, threaded=True, host='0.0.0.0', port=5001)
