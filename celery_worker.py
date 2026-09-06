from src import create_app
from src.extensions  import celery

app = create_app()

class FlaskTask(celery.Task):

    def __call__(self, *args, **kwargs):
        with app.app_context():
            return self.run(*args, **kwargs)


celery.Task = FlaskTask