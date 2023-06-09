#!/usr/bin/env python3

import sys
import json
from threading import Thread
from pprint import pprint

from pika.exceptions import ChannelClosedByBroker
from pika.exceptions import ChannelClosed

from broker import Consumer
from control import TestbedControl
from allocator import TestbedResourceAllocator

from models import TestbedModel
from models import MoteModel

from database import Database

from protocol import decoder
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

    Thread(target=analyze_message, args=(msg,)).start()


def analyze_message(msg: 'dict'):

    print('request received.')

    if decoder.check_message_format(msg):

        action = msg['action']
        testbedName = msg['testbed']

        if action == 'start':

            print('request is a start request.')

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
            stop_testbed(testbedName)

    else:
        print('request fail in format check stage.')


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

    fail = False

    motes = TestbedResourceAllocator.alloc_motes(moteCount)

    try:

        hopseq = [int(ch) for ch in hopseq.split(',') if ch]

        testbed = TestbedModel(
            name=name,
            motes=motes,
            analyzeIntv=analyzeIntv,
            txPower=txPower,
            txIntv=txIntv,
            hopseqLen=hsLen,
            hopseq=hopseq
        )

    except AssertionError:

        print(
            'request fail in start testbed stage. ',
            '(testbed already exists)'
        )

        fail = True

    else:

        control = TestbedControl(testbed)

        testbeds[testbed.name] = control

        if not control.start_testbed():
            print('request fail in start testbed stage.')
            fail = True

        else:
            print('start testbed with config:', end='')
            pprint(testbed.to_dict(), sort_dicts=False)

    if fail:
        for mote in motes:
            MoteModel.delete_mote(mote.id)


def stop_testbed(name: 'str'):
    global testbeds

    if name in testbeds:
        if testbeds[name].stop_testbed():
            print(f'stop testbed {name}.')
        else:
            print('request fail in stop testbed stage.')


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
        Database.reset()

        main()

    except (ChannelClosedByBroker, ChannelClosed):
        main()

    except KeyboardInterrupt as ki:
        print('testbed tsch control entity closed.')
        consumer.close()
        sys.exit(0)
