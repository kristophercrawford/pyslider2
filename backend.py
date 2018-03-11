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
              Column('insertTime', DateTime, server_default=func.now()),
              Column('direction', Integer),
              Column('shots', Integer),
              Column('timeDelay', Integer),
              Column('status', Integer),
    )
    t.create()

app = Flask(__name__)
api = Api(app)

# This function accepts a task number and will send back a 404 message if that task doesn't exist
def shortCircut(taskNumber):
    sql = e.connect()
    query = sql.execute("select exists(select 1 from tasks where id='{}')".format(taskNumber))
    r = query.fetchone()
    n = int(r[0])
    if n != 1:
        abort(404, message="Oh snap, task {} doesn't exist".format(taskNumber))

class taskList(Resource):
    def get(self):
        sql = e.connect()
        query = sql.execute("select id from tasks")
        data = [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]
        return data


    def put(self):
        sql = e.connect()
        direction = request.form['direction']
        shots = request.form['shots']
        timeDelay = request.form['timeDelay']
        sql.execute("insert into tasks (`direction`, `shots`, `timeDelay`) values ('{}', '{}', '{}')".format(direction, shots, timeDelay))
        return


class taskDetail(Resource):
    def get(self, taskNumber):
        shortCircut(taskNumber)
        sql = e.connect()
        query = sql.execute("select * from tasks where id='{}'".format(taskNumber))
        result = [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]
        return result


    def delete(self, taskNumber):
        shortCircut(taskNumber)
        sql = e.connect()
        sql.execute("delete from tasks where id='{}'".format(taskNumber))
        return


    def put(self, taskNumber):
        shortCircut(taskNumber)
        sql = e.connect()
        status = request.form['status']
        sql.execute("update tasks set status='{}' where id='{}'".format(status, taskNumber))
        return


class nextTask(Resource):
    def get(self):
        sql = e.connect()
        query = sql.execute("select * from tasks order by insertTime asc limit 1")
        result = [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]
        return result


api.add_resource(taskList, '/tasks')
api.add_resource(taskDetail, '/tasks/<int:taskNumber>')
api.add_resource(nextTask, '/nexttask')

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
