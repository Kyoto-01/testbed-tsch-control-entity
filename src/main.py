#!/usr/bin/env python3

import sys
import json
from threading import Thread
from pprint import pprint

from broker import Consumer
from control import TestbedControl
from allocator import TestbedResourceAllocator

from models import TestbedModel
from models import MoteModel

from utils.config import configure_from_file


CONFIG_FILE = "../config.ini"


conf = {}

testbeds = {}

consumer = None


def configure():
    global conf

    conf = configure_from_file(CONFIG_FILE)


def callback(ch, method, properties, body):
    msg = json.loads(body)

    Thread(target=analyze_message, args=(msg,))


def analyze_message(msg: 'dict'):
    action = msg['action']
    testbedName = msg['testbed']

    if action == 'start':

        moteCount = int(msg['provision']['mote_count'])
        txPower = int(msg['provision']['tx_power'])
        txIntv = float(msg['provision']['tx_intv'])
        hsLen = int(msg['provision']['hs_len'])
        hopseq = msg['provision']['hopseq']
        analyzeIntv = float(msg['provision']['analyze_intv'])

        start_testbed(
            name=testbedName,
            moteCount=moteCount,
            txPower=txPower,
            txIntv=txIntv,
            hsLen=hsLen,
            hopseq=hopseq,
            analyzeIntv=analyzeIntv
        )

    elif action == 'stop':
        stop_testbed()


def start_testbed(
    name: 'str',
    moteCount: 'int',
    txPower: 'int',
    txIntv: 'float',
    hsLen: 'int',
    hopseq: 'str',
    analyzeIntv: 'float'
):
    global testbeds

    motes = TestbedResourceAllocator.alloc_motes(moteCount)

    testbed = TestbedModel(
        name=name,
        motes=motes,
        analyzeIntv=analyzeIntv,
        txPower=txPower,
        txIntv=txIntv,
        hopseqLen=hsLen,
        hopseq=hopseq
    )

    control = TestbedControl(testbed)

    testbeds[testbed.name] = control

    if not control.start_testbed():
        for mote in motes:
            MoteModel.delete_mote(mote.id)
    else:
        print('start testbed with config:', end='')
        pprint(testbed.to_dict(), sort_dicts=False)


def stop_testbed(name: 'str'):
    global testbeds

    if name in testbeds:
        if testbeds[name].stop_testbed():
            print(f'stop testbed {name}.')


def main():
    global consumer

    configure()
    
    print('testbed tsch control entity started.')
    print('waiting for testbed control requests...')

    consumer = Consumer(
        host=conf['addr'],
        port=conf['port'],
        queue=conf['queue'],
        callback=callback
    )

    consumer.start()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt as ki:
        print('testbed tsch control entity closed.')
        consumer.close()
        sys.exit(0)
