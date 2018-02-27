from flask import Flask, request
from flask_restful import Resource, Api, abort
from sqlalchemy import create_engine
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

def short_circut(task_number):
    sql = e.connect()
    query = sql.execute("select exists(select 1 from tasks where id='%s')"%task_number)
    r = query.fetchone()
    n = int(r[0])
    if n != 1:
        abort(404, message="Oh snap, task {} doesn't exist".format(task_number))

class task_list(Resource):
    def get(self):
        sql = e.connect()
        query = sql.execute("select id from tasks")
        data = [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]
        return data

    def put(self):
        sql = e.connect()
        data = request.form['data']
        sql.execute("insert into tasks (`task_data`) values ('%s')"%data)
        return

class task_detail(Resource):
    def get(self, task_number):
        short_circut(task_number)
        sql = e.connect()
        query = sql.execute("select * from tasks where id='%s'"%task_number)
        result = [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]
        return result

    def delete(self, task_number):
        short_circut(task_number)
        sql = e.connect()
        sql.execute("delete from tasks where id='%s'" % task_number)
        return

api.add_resource(task_list, '/tasks')
api.add_resource(task_detail, '/tasks/<int:task_number>')

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
