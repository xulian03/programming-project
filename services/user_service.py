from project import User, Coach
from database.repository import RepositoryProvider

class UserService:

    def register_user(self, id, name, age, clazz):
        if self.user_repo.find(id):
            raise ValueError("El usuario ya existe")
        
        if age <= 0:
            raise ValueError("Edad inválida")

        user = RepositoryProvider.get(clazz.__name__)
        return user

    def login_user(self, id):
        user = self.user_repo.find(id)
        if not user:
            raise ValueError("Usuario no encontrado")
        return user