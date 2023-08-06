from click import echo

def log_error(message):
    echo("Error: {}".format(message), err=True)

