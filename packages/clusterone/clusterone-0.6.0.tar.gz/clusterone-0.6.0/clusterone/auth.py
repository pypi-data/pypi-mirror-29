from clusterone.config import Config

import functools


def authenticate():
    def decorator(f):

        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            try:
                config = args[0].config
            except:
                config = Config()
                config.__init__()
                config.load()

            username = config.get('username')
            token = config.get('token')
            if username == '' or token == '':
                print("You are not logged in yet. Use 'tport login'.")
                return
            return f(*args, **kwargs)

        return wrapper

    return decorator

