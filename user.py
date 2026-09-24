# Based on Prof Macarty's Python OOP tutorials: parts 1-4.
# https://github.com/mjmacarty/intro-python-oop

import datetime as dt
import hashlib
from dateutil import parser


class User:
    def __init__(self, username=None, password=None, email=None, birthday=None):
        self._username = username
        self.password = self._encrypt_password(password)
        self.email = email
        self.birthday = birthday

    def __str__(self):
        return (f"Username: {self.username}\nPassword: {self.password}\n"
                f"Email: {self.email}\nAge: {self.get_age()}")

    def __repr__(self):
        return f"{self.__class__.__name__}{self.__dict__}"

    def __eq__(self, other):
        return self.username == other.username

    def _encrypt_password(self, password):
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    def check_password(self, password):
        return self._encrypt_password(password) == self.password

    def get_age(self):
        birthday = parser.parse(self.birthday)
        return (dt.datetime.now() - birthday).days // 365

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, username):
        if not username:
            raise Exception("Username cannot be empty")
        self._username = username
