from flask import Flask, flash, render_template, request, redirect, jsonify, url_for, json
from flask_restful import Api, Resource
import requests

app = Flask(__name__)

@app.route('/task_summary')
def task_summary():
    task_list = requests.get('http://127.0.0.1:5000/tasks')
    return render_template('test.html', table=task_list.json())

@app.route('/task_detail')
def task_detail():
    task_list = requests.get('http://127.0.0.1:5000/tasks')

    # Initalize a counter
    counter = 0

    for task in task_list.json():
        row = task['id']
        req = requests.get('http://127.0.0.1:5000/tasks/%s'%row)
        #Increment the counter
        counter += 1
        if counter >= 2:
            b = req.json()
            # Extend array
            a.extend(b)
        else:
            a = req.json()
    return render_template('test.html', table2=a)

if __name__ == '__main__':
    app.run(debug=True, threaded=True, host='0.0.0.0', port=5001)
