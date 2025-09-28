from .repository import Repository
from project import Serializable
import json
import os

class JSONRepository(Repository):
    def __init__(self, cls: Serializable):
        self.cls = cls
        folder = "data"
        os.makedirs(folder, exist_ok=True)
        self.filename = os.path.join(folder, f"{cls.__name__.lower()}s.json")
        if not os.path.exists(self.filename):
            with open(self.filename, "w") as f:
                json.dump([], f)
    
    def _load(self):
        with open(self.filename, "r") as f:
            return json.load(f)

    def _save(self, data):
        with open(self.filename, "w") as f:
            json.dump(data, f, indent=2)

    def find(self, id):
        data = self._load()
        for element in data:
        
            if element["_id"] == id:
                return self.cls.deserialize(element)
        return None
    
    def findAll(self):
        return [self.cls.deserialize(element) for element in self._load]

    def save(self, element):
        data: list = self._load()
        id = element.get_id()

        for e in data:
            if e["_id"] == id:
                return False
        data.append(element.serialize())
        self._save(data)
        return True

    def delete(self, id):
        data = self._load()
        new_data = [d for d in data if d["_id"] != id]
        self._save(new_data)

    def replace(self, id, element):
        data = self._load()
        for i, d in enumerate(data):
            if d["_id"] == id:
                data[i] = self.cls.serialize(element)
                break
        self._save(data)