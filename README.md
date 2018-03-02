# pyslider2

Run the following command to populate database with sample task data.

`curl 127.0.0.1:5000/tasks -d "data=This task was inserted at $(date)" -X PUT`

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
        "insert_time": "2018-02-27 12:55:17",
        "task_data": "This task was inserted at Tue 27 Feb 07:55:17 EST 2018",
        "id": 3
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
