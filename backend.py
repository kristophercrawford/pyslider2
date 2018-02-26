from flask import Flask, request
from flask_restful import Resource, Api, abort
from sqlalchemy import create_engine
from json import dumps
import sqlite3


# Create sqlite database
conn = sqlite3.connect('example.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS tasks(id INTEGER PRIMARY KEY AUTOINCREMENT, insert_time DATETIME DEFAULT current_timestamp, task_data TEXT)''')
conn.commit()
conn.close()

# Open connection to database
e = create_engine('sqlite:///example.db')

    
app = Flask(__name__)
api = Api(app)

def abort_if_not_exist(task_number):
    conn = e.connect()
    query = conn.execute("select id from tasks")
    if task_number not in query:
        abort(404, message="Oh snap, task {} doesn't exist".format(task_number))

class task_list(Resource):
    def get(self):
        conn = e.connect()
        query = conn.execute("select id from tasks")
        return {'task_id': [i[0] for i in query.cursor.fetchall()]}

    def put(self):
        conn = e.connect()
        data = request.form['data']
        conn.execute("insert into tasks (`task_data`) values ('%s')"%data)
        return

class task_detail(Resource):
    def get(self, task_number):
        abort_if_not_exist(task_number)
        conn = e.connect()
        query = conn.execute("select * from tasks where id='%s'"%task_number)
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return result

    def delete(self, task_number):
        abort_if_not_exist(task_number)
        conn = e.connect()
        conn.execute("delete from tasks where id='%s'" % task_number)
        return

api.add_resource(task_list, '/tasks')
api.add_resource(task_detail, '/tasks/<string:task_number>')

if __name__ == '__main__':
    app.run(threaded=True)
