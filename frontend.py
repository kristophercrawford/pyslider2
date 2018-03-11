from flask import Flask, flash, render_template, request, redirect, jsonify, url_for, json
from flask_restful import Api, Resource, abort
import requests

app = Flask(__name__)


@app.route('/')
def homepage():
    return render_template('home.html')


@app.route('/status')
def statusPage():
    task_list = requests.get('http://127.0.0.1:5000/tasks')
    # If there are no tasks, return no data
    if not task_list.json():
        return render_template('status.html')
    # If there is one task, gather the details and return the data
    elif len(task_list.json()) == 1:
        detail = requests.get('http://127.0.0.1:5000/tasks/{}'.format(task_list.json()[0]['id']))
        return render_template('status.html', table=detail.json())
    # If there are multiple tasks, iterate through each task
    else:
        detail = []
        for task in task_list.json():
            row = task['id']
            # Extend list
            detail.extend(requests.get('http://127.0.0.1:5000/tasks/{}'.format(row)).json())
        return render_template('status.html', table=detail)


@app.route('/linear')
def linearSliderPage():
    return render_template("linear.html")


# Route for accepting posted data from forms
@app.route('/postdata', methods=['POST'])
def postdata():
    formInput = request.form
    print(request.form)
    timeDelay = formInput['timeDelay']
    direction = formInput['direction']
    shots = formInput['shots']
    requests.put('http://127.0.0.1:5000/tasks', data = {'timeDelay':timeDelay, 'direction':direction, 'shots':shots})
    return url_for('statusPage')


if __name__ == '__main__':
    app.run(debug=True, threaded=True, host='0.0.0.0', port=5001)
