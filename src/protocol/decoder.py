
def check_message_format(msg: 'dict'):
    ret = True

    try:
        assert 'action' in msg

        assert msg['action'] == 'start' or msg['action'] == 'stop'

        assert 'testbed' in msg

        if msg['action'] == 'start':

            assert 'provision' in msg

            assert 'mote_count' in msg['provision']
            assert 'tx_power' in msg['provision']
            assert 'tx_intv' in msg['provision']
            assert 'hs_len' in msg['provision']
            assert 'hopseq' in msg['provision']
            assert 'analyze_intv' in msg['provision']
    
    except AssertionError:
        ret = False

    return ret
