import re

from dict_validator.fields import String


class Email(String):
    """
    Make sure that the input is a valid email.

    :param domain: string representing a desired domain name. e.g. "gmail.com"
        if not present matches any domain name

    >>> from dict_validator import validate, deserialize

    >>> class Schema:
    ...     field = Email()

    >>> list(validate(Schema, {"field": "test@example.com"}))
    []

    >>> list(validate(Schema, {"field": "test.foo@example.bla.com"}))
    []

    >>> list(validate(Schema, {"field": "test123@examp123e.com"}))
    []

    >>> list(validate(Schema, {"field": "test-dff@example-ff.com"}))
    []

    >>> list(validate(Schema, {"field": "test%%20dff@example-ff.com"}))
    []

    >>> list(validate(Schema, {"field": "test+20dff@example-ff.com"}))
    []

    Missing domain:

    >>> list(validate(Schema, {"field": "test@"}))
    [(['field'], 'Did not match Regexp(email)')]

    Missing beginning:

    >>> list(validate(Schema, {"field": "@example-ff.com"}))
    [(['field'], 'Did not match Regexp(email)')]

    Wrong beginning:

    >>> list(validate(Schema, {"field": "~~~@example.bla.com"}))
    [(['field'], 'Did not match Regexp(email)')]

    Wrong domain:

    >>> list(validate(Schema, {"field": "test123@examp++e.com"}))
    [(['field'], 'Did not match Regexp(email)')]

    No @ char:

    >>> list(validate(Schema, {"field": "fdfdfdgdg"}))
    [(['field'], 'Did not match Regexp(email)')]

    Specify a domain:

    >>> class Schema:
    ...     field = Email(domain="example.com")

    >>> list(validate(Schema, {"field": "test@example.com"}))
    []

    Wrong domain:

    >>> list(validate(Schema, {"field": "test@not-example.com"}))
    [(['field'], 'Did not match Regexp(email)')]

    >>> deserialize(Schema, {"field": "foobar@EXAMPLE.com"}).field
    'foobar@example.com'

    """

    def __init__(self, domain=None, **kwargs):
        if domain:
            domain = re.escape(domain)
        else:
            domain = r"(?:[a-zA-Z0-9-]+\.)+[a-z]{2,}"
        super(Email, self).__init__(
            r"^[a-zA-Z0-9._%+-]+@{}$".format(domain),
            "email", **kwargs)

    def deserialize(self, value):
        # Make sure that the domain name is always in lower case
        parts = value.split("@", 1)
        return "@".join([parts[0], parts[1].lower()])
