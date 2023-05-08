#!/usr/bin/env python3

from pprint import pprint

from allocator import TestbedResourceAllocator
from models import TestbedModel
from control import TestbedControl
from database import Database


CONFIG_PATH = '../config.ini'


testbeds = {}


def start_testbed(
    name: 'str',
    moteCount: 'int',
    analyzeIntv: 'int',
    txPower: 'int',
    txIntv: 'float',
    hopseqLen: 'int',
    hopseq: 'list[int]',
):
    global testbeds

    motes = TestbedResourceAllocator.alloc_motes(moteCount)

    testbed = TestbedModel(
        name=name,
        motes=motes,
        analyzeIntv=analyzeIntv,
        txPower=txPower,
        txIntv=txIntv,
        hopseqLen=hopseqLen,
        hopseq=hopseq
    )

    print('start testbed with config:', end='')
    pprint(testbed.to_dict(), sort_dicts=False)

    control = TestbedControl(testbed)

    testbeds[testbed.name] = control
    
    control.start_testbed(verbose=True)


def main():
    global testbeds

    print('What do you want to do?')
    print('[1] start a new testbed')
    print('[2] stop an existing testbed')
    print('[3] List existing testbeds')

    option = input('->')

    try:
        if option == '1':
            name = input('testbed name ->')

            moteCount = input('testbed mote count ->')
            if not moteCount:
                moteCount = '2'
            moteCount = int(moteCount)

            analyzeIntv = input('testbed analyze interval ->')
            if not analyzeIntv:
                analyzeIntv = '60'
            analyzeIntv = int(analyzeIntv)

            txPower = input('testbed clients tx power ->')
            txIntv = input('testbed clients tx interval ->')
            hopseqLen = input('testbed motes hop sequence length ->')
            hopseq = input('testbed clients hop sequence ->').split(',')

            start_testbed(
                name=name,
                moteCount=moteCount,
                analyzeIntv=analyzeIntv,
                txPower=txPower,
                txIntv=txIntv,
                hopseqLen=hopseqLen,
                hopseq=hopseq
            )
        elif option == '2':
            name = input('testbed name ->')

            if name in testbeds:
                testbeds[name].stop_testbed(verbose=True)
        elif option == '3':
            testbedList = [t.testbed for t in testbeds.values()]
            pprint(testbedList, sort_dicts=False)
        else:
            print('Invalid option.')

    except Exception as ex:
        Database.set_collections(prevData)
        raise ex


prevData = Database.get_collections()

while True:
    try:
        main()
    except KeyboardInterrupt as ki:
        Database.set_collections(prevData)
        break
    except Exception as ex:
        raise ex
