from .celery import app


@app.task
def add():
    print("Hello", "World!")
