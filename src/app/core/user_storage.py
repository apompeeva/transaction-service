from dataclasses import dataclass, field
from decimal import Decimal


@dataclass
class User():
    id: int
    verified: bool = False
    _balance: Decimal = 0

    @property
    def balance(self):
        return self._balance

    def is_verified(self):
        return self.verified

    def update_balance(self, new_balance):
        self._balance = new_balance


class UserStorage():
    _storage: dict[int, User] = {
        1: User(1, False, 0),
        2: User(2, True, 100),
    }

    def add_user():
        pass

    def get_user(self, user_id: int) -> User:
        return self._storage[user_id]

    def update_user(self, user: User):
        self._storage[user.id] = user
