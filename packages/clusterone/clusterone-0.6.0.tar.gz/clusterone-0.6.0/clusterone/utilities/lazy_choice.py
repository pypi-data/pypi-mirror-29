from click import Choice


class LazyChoice(Choice):
    """
    Just like click.Choice except it takes a callable instead of an array
    The callable is evaulated only when needed, not at every CLI execution
    """

    def __init__(self, choice_callable):
        self._choices = choice_callable

    @property
    def choices(self):
        """
        Caution: This must return array of strings
        """

        return self._choices()
