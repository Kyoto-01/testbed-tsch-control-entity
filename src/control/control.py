import subprocess

from models import TestbedModel
from models import MoteModel


class TestbedControl:

    def __init__(
        self,
        testbed: 'TestbedModel',
    ):
        self._testbed = testbed

    @property
    def testbed(self):
        return self._testbed.to_dict()

    def _destroy_testbed_environment(self):
        ret = True

        if self._testbed.motes:

            cmd = [
                'docker',
                'stop',
                self._testbed.name
            ]

            output = subprocess.run(args=cmd)

            if not output or output.returncode != 0:
                ret = False

        return ret

    def start_testbed(self):

        ret = False

        mainAnalyzeIntv = 60

        ports = [m.port for m in self._testbed.motes]
        ports = ','.join(ports)

        hopseq = [str(h) for h in self._testbed.hopseq]
        hopseq = ','.join(hopseq)

        if ports:

            cmd = [
                'docker',
                'run',
                '-d',
                '-v',
                '/dev:/dev',
                '--name',
                self._testbed.name,
                '--privileged',
                '--rm',
                'testbed-experiment:1.0',
                './control.sh',
                '--action',
                'start',
                '--usbports',
                ports,
                '--testbed',
                self._testbed.name
            ]

            cmd += ['--firmtxpwr', str(self._testbed.txPower)] \
                if self._testbed.txPower else []

            cmd += ['--firmtxintv', str(self._testbed.txIntv)] \
                if self._testbed.txIntv else []

            # Less priority than --firmhopseq
            cmd += ['--firmhslen', str(self._testbed.hopseqLen)] \
                if self._testbed.hopseqLen and not hopseq else []

            cmd += ['--firmhopseq', hopseq] \
                if hopseq else []

            cmd += ['--analyzeintv', str(self._testbed.analyzeIntv)] \
                if self._testbed.analyzeIntv \
                else ['--analyzeintv', str(mainAnalyzeIntv)]

            output = subprocess.run(args=cmd)

            if not output or output.returncode != 0:
                self._destroy_testbed_environment()
            else:
                TestbedModel.insert_testbed(self._testbed)
                ret = True

        return ret

    def stop_testbed(self):
        ret = True

        ports = [m.port for m in self._testbed.motes]
        ports = ','.join(ports)

        if ports:

            TestbedModel.delete_testbed(self._testbed.id)

            for mote in self._testbed.motes:
                MoteModel.delete_mote(mote.id)

            cmd = [
                'docker',
                'exec',
                self._testbed.name,
                './control.sh',
                '--action',
                'stop',
                '--usbports',
                ports,
                '--testbed',
                self._testbed.name,
            ]

            output = subprocess.run(args=cmd)

            if not output or output.returncode != 0:
                ret = False

        else:
            ret = False

        return ret
