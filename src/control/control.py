import subprocess


class TestbedConstants:

    def __init__(
        self,
        name: 'str',
        txPower: 'int' = 3,
        txIntv: 'float' = 5,
        hopseqLen: 'int' = 0,
        hopseq: 'list' = []
    ):
        self.name = name
        self.txPower = txPower
        self.txIntv = txIntv
        self.hopseqLen = hopseqLen
        self.hopseq = hopseq


class TestbedProcess:

    def __init__(
        self,
        name: 'str' = None,
        path: 'str' = None,
        pid: 'int' = 0
    ):
        self.name = name
        self.path = path
        self.pid = pid


class TestbedControl:

    def __init__(
        self,
        testbed: 'TestbedConstants',
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
        cmd = (
            f'{self._buildTool.path}' +
            f'-f all' +
            f'-p {self._testbed.txPower}' +
            f'-i {self._testbed.txIntv}' +
            f'-l {self._testbed.hopseqLen}' +
            f'-h {self._testbed.hopseq}'
        )

        subprocess.run()

    def stop_motes_firmware(self):
        pass

    def start_serial_reader(self):
        pass

    def stop_serial_reader(self):
        pass

    def start_rpc_client(self):
        pass

    def stop_rpc_client(self):
        pass
