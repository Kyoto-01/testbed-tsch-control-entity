from subprocess import Popen, PIPE, STDOUT
from random import randint

from data_access import Database
from utils.sys_info import get_sys_serial_devices


class TestbedConstants:

    def __init__(
        self,
        txPower: 'int' = 3,
        txIntv: 'float' = 5,
        hopseqLen: 'int' = 0,
        hopseq: 'list' = []
    ):
        self._txPower = txPower
        self._txIntv = txIntv
        self._hopseqLen = hopseqLen
        self._hopseq = hopseq
    
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


class Testbed:

    def __init__(
        self,
        name: 'str',
        moteCount: 'int',
        constants: 'TestbedConstants'
    ):
        self._name = name
        self._moteCount = moteCount
        self._constants = constants

    @property
    def name(self):
        return self._name
    
    @property
    def moteCount(self):
        return self._moteCount
    
    @property
    def constants(self):
        return self._constants


class TestbedControl:

    def __init__(
        self,
        testbed: 'Testbed',
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

    def alloc_devices(self, count: 'int') -> 'list':
        data = Database.get_collections()
        devices = get_sys_serial_devices()
        busyDevices = data['resources']['busy_ports']

        chosenDevices = []

        availableDeviceCount = len(devices) - len(busyDevices)

        if availableDeviceCount >= count:
            while len(chosenDevices) < count:
                rand = randint(0, len(devices))
                dev = devices[rand]

                if dev not in busyDevices:
                    chosenDevices.append(dev)
                    busyDevices.append(dev)

        data['resources']['busy_ports'] = busyDevices

        return chosenDevices

    def start_motes_firmware(self):
        devices = self.alloc_devices(self._testbed.moteCount)

        args = (
            f'-f all' +
            f'-p {self._testbed.constants.txPower}' +
            f'-i {self._testbed.constants.txIntv}' +
            f'-l {self._testbed.constants.hopseqLen}' +
            f'-h {self._testbed.constants.hopseq}'
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
