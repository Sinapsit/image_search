import abc


class VectorAbstract(metaclass=abc.ABCMeta):
    def __init__(self, image=None):
        self.image = image

    @abc.abstractmethod
    def get_vector(self):
        pass

    @abc.abstractmethod
    def get_similar(self, queryset=None):
        pass


class SearchByVector(VectorAbstract):
    """Base VectorSearch class."""

    def get_vector(self):
        return 'test'

    def get_similar(self, queryset=None):
        return queryset
