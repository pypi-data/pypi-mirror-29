from dict_validator import Field


class Number(Field):
    """
    Match integers, floats and longs

    :param min: the smallest number allowed
    :param max: the largest number allowed
    :param can_be_float: True if the number can contain a dot

    >>> from dict_validator import validate, describe

    >>> class Schema:
    ...     field = Number(min=10, max=20)

    >>> list(validate(Schema, {"field": 15}))
    []

    >>> list(validate(Schema, {"field": 5}))
    [(['field'], 'Too small')]

    >>> list(validate(Schema, {"field": 25}))
    [(['field'], 'Too large')]

    The number has to be passed as a digit.

    >>> list(validate(Schema, {"field": "15"}))
    [(['field'], 'Not a valid number')]

    >>> from pprint import pprint

    >>> pprint(list(describe(Schema)), width=50)
    [([], {'type': 'Dict'}),
     (['field'],
      {'can_be_float': True,
       'max': 20,
       'min': 10,
       'type': 'Number'})]

    To disable floats - set can_be_float to False (it is True by default).

    >>> class Schema:
    ...     field = Number(can_be_float=False)

    >>> list(validate(Schema, {"field": 15.0}))
    [(['field'], 'Not a valid number')]

    """

    # pylint: disable=redefined-builtin
    def __init__(self, min=None, max=None, can_be_float=True, **kwargs):
        super(Number, self).__init__(**kwargs)
        self._min = min
        self._max = max
        self._can_be_float = can_be_float

    def _validate(self, value):
        allowed_types = (int, int)
        if self._can_be_float:
            allowed_types += (float,)

        if not isinstance(value, allowed_types):
            return "Not a valid number"

        if self._min is not None and value < self._min:
            return "Too small"

        if self._max is not None and value > self._max:
            return "Too large"
        return None

    def _describe(self):
        return {
            "min": self._min,
            "max": self._max,
            "can_be_float": self._can_be_float
        }
