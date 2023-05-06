from uuid import uuid4

from database import Database
from models import MoteModel


class TestbedModel:

    def __init__(
        self,
        name: 'str',
        motes: 'list[MoteModel]',
        txPower: 'int',
        txIntv: 'float',
        hopseqLen: 'int',
        hopseq: 'list[int]',
        id: 'str' = uuid4()
    ):
        self._id = id
        self._name = name
        self._motes = motes
        self._txPower = txPower
        self._txIntv = txIntv
        self._hopseqLen = hopseqLen
        self._hopseq = hopseq

    @property
    def id(self):
        return self._id
    
    @property
    def name(self):
        return self._name
    
    @property
    def motes(self):
        return self._motes
    
    @property
    def txPower(self):
        return self._txPower
    
    @property
    def txIntv(self):
        return self._txIntv
    
    @property
    def hopseqLen(self):
        return self._hopseqLen

    @property
    def hopseq(self):
        return self._hopseq
    
    def to_dict(self) -> 'dict':
        data = {
            'id': self._id,
            'name': self._name,
            'motes': self._motes,
            'tx_power': self._txPower,
            'tx_intv': self._txIntv,
            'hop_seq_len': self._hopseqLen,
            'hopseq': self._hopseq
        }

        return data
    
    @staticmethod
    def from_dict(data: 'dict') -> 'TestbedModel':
        data = TestbedModel(
            id=data['id'],
            name=data['name'],
            motes=data['motes'],
            txPower=data['tx_power'],
            txIntv=data['tx_intv'],
            hopseqLen=data['hop_seq_len'],
            hopseq=data['hopseq']
        )

        return data

    @staticmethod
    def select_testbeds() -> 'dict[str, TestbedModel]':
        collections = Database.get_collections()
        collections = collections['resources']['testbeds']

        data = {}

        for record in collections.values():
            record = TestbedModel.from_dict(record)
            data[record.id] = record

        return data

    @staticmethod
    def insert_testbed(data: 'TestbedModel') -> 'str':
        collections = Database.get_collections()

        if data.id:
            collections['resources']['testbeds'][data.id] = data.to_dict()

            Database.set_collections(collections)

        return data.id

    @staticmethod
    def delete_testbed(id: 'str') -> 'str':
        collections = Database.get_collections()

        if id in collections['resources']['testbeds']:
            del collections['resources']['testbeds'][id]

            Database.set_collections(collections)

        return id
