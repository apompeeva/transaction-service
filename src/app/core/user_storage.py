from dataclasses import dataclass
from decimal import Decimal


@dataclass
class User():
    """Данные пользователя."""

    id: int
    verified: bool = False
    _balance: Decimal = Decimal(0)

    @property
    def balance(self):
        """Остаток по счету."""
        return self._balance

    def is_verified(self):
        """Верифицирован ли пользователь."""
        return self.verified

    def update_balance(self, new_balance):
        """Обновить остаток по счету."""
        self._balance = new_balance


class UserStorage():
    """Хранилище пользователей."""

    _storage: dict[int, User] = {}

    def add_user(self, user_id):
        """Добавить пользователя в хранилище."""
        self._storage.update({user_id: User(user_id)})

    def get_user(self, user_id: int) -> User:
        """Получить данные пользователя из хранилища."""
        return self._storage[user_id]

    def update_user(self, user: User):
        """Обновить данные пользователя."""
        self._storage[user.id] = user
