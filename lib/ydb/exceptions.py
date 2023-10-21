from lib.exceptions import DetailException


class ToDoExceptions(Exception):
    ...

class DatabaseError(ToDoExceptions):
    "Database error"
    def __init__(self):
        raise DetailException('Database error')
