from flask import Flask, request
from flask_restful import Resource, Api, abort
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, DateTime, func, String

# Open connection to database and create database and table if one is not present
e = create_engine('sqlite:///example.db')
metadata = MetaData(e)

if not e.dialect.has_table(e, 'tasks'):
    t = Table('tasks', metadata,
          Column('id', Integer, primary_key=True, nullable=False),
          Column('insert_time', DateTime, server_default=func.now()),
          Column('task_data', String(128)),
    )
    t.create()

app = Flask(__name__)
api = Api(app)

# This function accepts a task number and will send back a 404 message if that task doesn't exist
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
