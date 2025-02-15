import environ

env = environ.Env(
    SECRET_KEY=(str, 'not-so-secret'),
    DEBUG=(bool, False)
)