from .celery import app


@app.task
def add() -> None:
    print("Hello", "World!")
