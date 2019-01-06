import abc
from collections import namedtuple


class Privilege(namedtuple('Privilege', ('name', 'description', 'categories')), metaclass=abc.ABCMeta):

    def __eq__(self, other):
        return isinstance(other, Privilege) and self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return f"{self.__class__.__name__}: {self.name}"

    def to_dict(self):
        return {'id': self.name,
                'name': self.name,
                'categories': self.categories,
                'description': self.description}
