from werkzeug import security
from flask_login import UserMixin
import json
import bcrypt

def make_key():
    return security.gen_salt(30)


class User(UserMixin):
    def __init__(self, username):
        self.username = username

    def get_id(self):
        return self.username


class JsonUserDatabase:

    def __init__(self, path):

        self.path = path
        self._api_keys = {}

        try:
            with open(path, 'r+') as f:
                data = f.read()
                self._users = json.loads(data).get('users')
        except IOError as e:
            self._users = {}
            self.__write()

        for username, user in self._users.iteritems():
            for key in user.get('keys', []):
                self._api_keys[key] = username

    def is_empty(self):
        return not bool(self._users)
                
    def validate(self, user, password):
        p = self._users.get(user, None)
        if p is None:
            return False
        else:
            stored_hash = p['password']
            hashed = bcrypt.hashpw(password, stored_hash)
            return stored_hash == hashed

    def load_from_apikey(self, key):
        u = self._api_keys.get(key)
        return User(u) if u is not None else None

    def add_apikey(self, username):
        u = self._users.get(username)
        if u is None:
            raise ValueError("Unknown user %s" % username)

        while True:
            key = make_key()
            if key not in self._api_keys:
                break

        keys = u.get('keys', [])
        keys.append(key)
        u.update({'keys': keys})

        self._api_keys[key] = username

        self.__write()
        return key

    def add(self, username, password):
        hashed_pass = bcrypt.hashpw(password, bcrypt.gensalt())
        self._users.update({username: {'password': hashed_pass}})

        self.__write()

    def __write(self):
        with open(self.path, 'w') as f:
            f.write(json.dumps({'users': self._users}, indent=4))


class TestUserDatabase:
    def __init__(self):
        self._api_keys = ['N92aERQgrH0xKmOE4mKm4w99sTQ9Fw']
        pass

    @staticmethod
    def validate(user, password):
        return security.safe_str_cmp(user, 'test') and\
                security.safe_str_cmp(password, 'test')

    def load_from_apikey(self, key):
        return User('test') if key in self._api_keys else None

    def add_apikey(self, username):
        if username != 'test':
            raise ValueError("Invalid username. Only 'test' allowed!")

        while True:
            key = make_key()
            if key not in self._api_keys:
                break

        self._api_keys.append(key)
