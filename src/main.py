#!/usr/bin/env python3

from pprint import pprint
from configparser import ConfigParser

from allocator import TestbedResourceAllocator
from models import TestbedModel
from control import TestbedControl
from database import Database


CONFIG_PATH = '../config.ini'


conf = {}


def configure_from_file():
    conf = ConfigParser()
    conf.read(CONFIG_PATH)
    conf = dict(conf)

    return conf

def start_testbed(
    name: 'str',
    moteCount: 'int',
    txPower: 'int',
    txIntv: 'float',
    hopseqLen: 'int',
    hopseq: 'list[int]',
):
    global conf

    motes = TestbedResourceAllocator.alloc_motes(moteCount)

    testbed = TestbedModel(
        name=name,
        motes=motes,
        txPower=txPower,
        txIntv=txIntv,
        hopseqLen=hopseqLen,
        hopseq=hopseq
    )

    print('start testbed with config:', end='')
    pprint(testbed.to_dict(), sort_dicts=False)

    control = TestbedControl(testbed, conf)
    
    control.start_testbed(verbose=True)


def main():
    global conf

    conf = configure_from_file()

    prevData = Database.get_collections()

    print('What do you want to do?')
    print('[1] start a new testbed')
    print('[2] stop an existing testbed')
    print('[3] List existing testbeds')

    option = input('->')

    try:
        if option == '1':
            name = input('testbed name ->')

            moteCount = int(input('testbed mote count ->'))
            txPower = input('testbed clients tx power ->')
            txIntv = input('testbed clients tx interval ->')
            hopseqLen = input('testbed motes hop sequence length ->')
            hopseq = input('testbed clients hop sequence ->').split(',')

            start_testbed(
                name=name,
                moteCount=moteCount,
                txPower=txPower,
                txIntv=txIntv,
                hopseqLen=hopseqLen,
                hopseq=hopseq
            )
        elif option == '2':
            ...
        elif option == '3':
            testbeds = TestbedModel.select_testbeds()
            pprint(testbeds, sort_dicts=False)
        else:
            ...

        Database.set_collections(prevData)
    except Exception as ex:
        Database.set_collections(prevData)
        raise ex


main()
