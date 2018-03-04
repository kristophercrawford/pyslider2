# pyslider2

Run the following command to populate database with sample task data.

`curl 127.0.0.1:5000/tasks -X PUT -d "shots=10" -d "direction=l2r" -d "time_delay=1" -d "start_time=2018-03-05 00:00:00"`

Run the following command to see a list of all task id's.

```
$ curl 127.0.0.1:5000/tasks
[
    {
        "id": 1
    },
    {
        "id": 2
    },
    {
        "id": 3
    }
]
```

To see a detailed view of a task, specify a task id in the request.

```
$ curl 127.0.0.1:5000/tasks/3
[
    {
        "id": 3,
        "insert_time": "2018-03-04 16:11:51",
        "start_time": "2018-03-04 00:00:00",
        "time_delay": 1,
        "direction": "l2r",
        "shots": 10,
        "status": null
    }
]
```

To delete a task, specify the task id with a DELETE request.

```
$ curl 127.0.0.1:5000/tasks/3 -X DELETE
null
$ curl 127.0.0.1:5000/tasks/3
{
    "message": "Oh snap, task 3 doesn't exist. You have requested this URI [/tasks/3] but did you mean /tasks/<int:task_number> or /tasks ?"
}
```

To update the status field of a task, specify the task id with a PUT request.

```
$ curl 127.0.0.1:5000/tasks/3 -X PUT -d "status=10"
null
$ curl 127.0.0.1:5000/tasks/3
[
    {
        "id": 3,
        "insert_time": "2018-03-04 16:11:51",
        "start_time": "2018-03-04 00:00:00",
        "time_delay": 1,
        "direction": "l2r",
        "shots": 10,
        "status": 10
    }
]
```
