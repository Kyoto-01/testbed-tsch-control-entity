from subprocess import Popen, PIPE, STDOUT

from models import TestbedModel


class TestbedProcess:

    def __init__(
        self,
        name: 'str' = None,
        path: 'str' = None,
    ):
        self._name = name
        self._path = path
        self._args : 'list' = None
        self._proc : 'Popen' = None

    @property
    def name(self):
        return self._name

    @property
    def path(self):
        return self._path
    
    def is_running(self):
        return self._proc is not None

    def run(self, args: 'list'):
        if not self.is_running():
            self._args = args

            cmd = [self._path]
            if self._args:
                cmd += self._args

            self._proc = Popen(
                args=cmd,
                stdin=PIPE,
                stdout=PIPE,
                stderr=STDOUT
            )

    def kill(self):
        if self.is_running():
            self._proc.kill()
            self._proc = None

    def restart(self):
        self.kill()
        self.run(self._args)


class TestbedControl:

    def __init__(
        self,
        testbed: 'TestbedModel',
        buildToolPath: 'str',
        serialReaderPath: 'str',
        rpcClientPath: 'str'
    ):
        self._testbed = testbed

        self._buildTool: 'TestbedProcess' = TestbedProcess(
            name='Testbed Build Tool',
            path=buildToolPath
        )

        self._serialReader: 'TestbedProcess' = TestbedProcess(
            name='Testbed Serial Reader',
            path=serialReaderPath
        )

        self._rpcClient: 'TestbedProcess' = TestbedProcess(
            name='Testbed RPC Client',
            path=rpcClientPath
        )

    def start_motes_firmware(self):
        ports = [m.port for m in self._testbed.motes]
        ports = ','.join(ports)

        hopseq = [str(h) for h in self._testbed.hopseq]
        hopseq = ','.join(self._testbed.hopseq)

        args = (
            f'-f all ' +
            f'-p {self._testbed.txPower} ' +
            f'-i {self._testbed.txIntv} ' +
            f'-l {self._testbed.hopseqLen} ' +
            f'-h {hopseq} ' +
            f'-u {ports}'
        )

        self._buildTool.run(args)

    def stop_motes_firmware(self):
        ports = [m.port for m in self._testbed.motes]
        ports = ','.join(ports)

        args = (
            f'-f stopped ' +
            f'-u {ports}'
        )

        self._buildTool.run(args)

    def start_serial_reader(self):
        pass

    def stop_serial_reader(self):
        pass

    def start_rpc_client(self):
        pass

    def stop_rpc_client(self):
        pass
