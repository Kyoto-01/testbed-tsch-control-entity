import re


def check_message_format(msg: 'dict'):
    ret = True

    try:
        assert 'action' in msg

        assert msg['action'] == 'start' or msg['action'] == 'stop'

        assert 'testbed' in msg

        if msg['action'] == 'start':

            assert 'provision' in msg

            assert 'mote_count' in msg['provision']
            int(msg['provision']['mote_count'])

            assert 'tx_power' in msg['provision']
            if msg['provision']['tx_power']:
                int(msg['provision']['tx_power'])

            assert 'tx_intv' in msg['provision']
            if msg['provision']['tx_intv']:
                float(msg['provision']['tx_intv'])

            assert 'hs_len' in msg['provision']
            if msg['provision']['hs_len']:
                int(msg['provision']['hs_len'])

            assert 'hopseq' in msg['provision']
            if msg['provision']['hopseq']:
                assert re.fullmatch(
                    r"[0-9]+(,[0-9]+)*", 
                    msg['provision']['hopseq']
                ) is not None

            assert 'analyze_intv' in msg['provision']
            if msg['provision']['analyze_intv']:
                float(msg['provision']['analyze_intv'])
    
    except AssertionError:
        ret = False

    return ret
