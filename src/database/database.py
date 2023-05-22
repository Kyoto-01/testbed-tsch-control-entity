import json
from threading import Lock


class Database:

    DATABASE_PATH = 'database/database.json'

    MUTEX = Lock()

    @staticmethod
    def get_collections() -> 'dict':
        data = None

        with Database.MUTEX:
            with open(Database.DATABASE_PATH, 'r') as f:
                data = f.read()
                data = json.loads(data)

        return data


    @staticmethod
    def set_collections(data: 'dict'):
        data = json.dumps(data)

        with Database.MUTEX:
            with open(Database.DATABASE_PATH, 'w') as f:
                f.write(data)
