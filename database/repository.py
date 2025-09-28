from abc import ABC, abstractmethod

class Repository(ABC):
    @abstractmethod
    def find(self, id):
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