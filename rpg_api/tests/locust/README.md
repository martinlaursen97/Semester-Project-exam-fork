# Locust Load Testing

Install:

```bash
pip install locust
```

Run:

```bash
locust
```

To run a specific task in the cli, we use the `@tag` offered by the Locust framework when creating the task.

This will run all tasks in the locustfile with the `@tag` set to "media":

```bash
locust --host http://localhost:8000 --tags media   
```

Running multiple tags, here we run all tasks tagged with "media" and "read":

```bash
locust --host http://localhost:8000 --tags media read   
```

It's also possible to exclude tasks, This will run all tasks, except the tasks that are tagged with "media":

```bash
locust --host http://localhost:8000 --exclude-tags media
```

To pick which class to run you can use --class-picker for the ui, or --class for the headless:

```bash
locust --host http://localhost:8000 --class-picker
locust --headless --host http://localhost:8000 --class QuickStartUser
```



Then open <http://localhost:8089> in your browser and start a test.

