from functools import partial, wraps

from click import Choice


def lazify(function):
    """
    Transforms an ordinary function to a callable that resolves to function's original value

    Idea: f(x): y -> f(x):f'(): y
    Particullarly usefull for methods, where x == self
    """

    @wraps(function)
    def wrapper(*args, **kwargs):
        return partial(function, *args, **kwargs)
    return wrapper

#TODO: Code this
#TODO: Test this
#TODO: Propagate this across client
def lazy_property(*args, **kwargs):
    """
    Convinience wrapper: combines @property and @lazify

    This will not work:
    `lazy_property = lazify(property)`

    But it conveyes the idea of a lazy_property

    Has to be done different way, not the best time now. Did workarounds.

    Usefull insights: https://stackoverflow.com/questions/47066728/combine-property-with-another-decorator
    """

    raise NotImplementedError()

class LazyChoice(Choice):
    """
    Just like click.Choice except it takes a callable instead of an array
    The callable is evaulated only when needed, not at every CLI execution
    """

    def __init__(self, choice_callable):
        self.__choices = choice_callable

    @property
    def choices(self):
        """
        Caution: This must return array of strings
        """

        return self.__choices()
