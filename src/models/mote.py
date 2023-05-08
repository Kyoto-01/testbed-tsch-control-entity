from uuid import uuid4

from database import Database


class MoteModel:

    def __init__(
        self,
        port: 'str',
        is_busy: 'bool',
        id: 'str' = None
    ):
        if not id:
            id = str(uuid4())

        self._id = id
        self._port = port
        self._is_busy = is_busy

    @property
    def id(self):
        return self._id
    
    @property
    def port(self):
        return self._port
    
    @property
    def is_busy(self):
        return self._is_busy
    
    def to_dict(self) -> 'dict':
        data = {
            'id': self._id,
            'port': self._port,
            'is_busy': self._is_busy
        }

        return data
    
    @staticmethod
    def from_dict(data: 'dict') -> 'MoteModel':
        data = MoteModel(
            id=data['id'],
            port=data['port'],
            is_busy=data['is_busy']
        )

        return data

    @staticmethod
    def select_motes() -> 'dict[str, MoteModel]':
        collections = Database.get_collections()
        collections = collections['resources']['motes']

        data = {}

        for record in collections.values():
            record = MoteModel.from_dict(record)
            data[record.id] = record

        return data
    
    @staticmethod
    def select_motes_by_busy(is_busy: 'bool') -> 'dict[str, MoteModel]':
        collections = Database.get_collections()
        collections = collections['resources']['motes']

        data = {}

        for record in collections.values():
            if record['is_busy'] == is_busy:
                record = MoteModel.from_dict(record)
                data[record.id] = record

        return data

    @staticmethod
    def insert_mote(data: 'MoteModel') -> 'str':
        collections = Database.get_collections()

        if data.id:
            collections['resources']['motes'][data.id] = data.to_dict()

            Database.set_collections(collections)

        return data.id

    @staticmethod
    def delete_mote(id: 'str') -> 'str':
        collections = Database.get_collections()
        collections = collections['resources']['motes']

        if id in collections['resources']['motes']:
            del collections['resources']['motes'][id]

            Database.set_collections(collections)

        return id