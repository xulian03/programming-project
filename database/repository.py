from abc import ABC, abstractmethod

class Repository(ABC):
    @abstractmethod
    def find(self, id):
        pass
    
    @abstractmethod
    def findAll(self):
        pass

    @abstractmethod
    def save(self, element):
        pass

    @abstractmethod
    def delete(self, id):
        pass

    @abstractmethod
    def replace(self, id, element):
        pass

class RepositoryProvider():
    _repositories = {}

    @classmethod
    def register(cls, name: str, repo):
        cls._repositories[name] = repo

    @classmethod
    def get(cls, name) -> Repository:
        if not name in cls._repositories.keys():
            return None
        return cls._repositories[name]