import abc


def all_subclasses(cls):
    return cls.__subclasses__() \
        + [g for s in cls.__subclasses__() for g in all_subclasses(s)]


class Converter(metaclass=abc.ABCMeta):
    """ A base class if we incorporate more converters in the future. New
    implementations need to be registered in this modules __init__.py """

    @abc.abstractmethod
    def convert(self):
        pass

    @property
    @abc.abstractclassmethod
    def accepted_files(cls):
        pass

    @classmethod
    def implementations(cls):
        return all_subclasses(cls)

    @classmethod
    def accept(cls, filepath):
        return any(filepath.endswith(ending) for ending in cls.accepted_files)
