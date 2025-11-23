from abc import ABC


class BaseModel(ABC):



    _next_id = 1

    def __init__(self, name):
        self._id = BaseModel._next_id
        BaseModel._next_id += 1
        self._name = name

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not value:
            raise ValueError("Name cannot be empty")
        self._name = value

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, name={self.name})"
