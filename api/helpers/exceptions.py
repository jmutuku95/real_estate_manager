"""
Custom exceptions.
"""


class ObjectNotFoundError(Exception):
    """
    To be raised in the event of an object not being available in the database.
    """

    def __init__(self):
        self.message = "The object does not exist."
