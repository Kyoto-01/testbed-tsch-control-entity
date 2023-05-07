from subprocess import Popen, PIPE, STDOUT

from models import TestbedModel


class TestbedProcess:

    def __init__(
        self,
        name: 'str' = None,
        path: 'str' = None
    ):
        self._name = name
        self._path = path
        self._args: 'list' = None
        self._proc: 'Popen' = None

    @property
    def name(self):
        return self._name

    @property

    def path(self):
        return self._path

    @property
    def pid(self):
        return self._proc.pid

    def is_running(self):
        return (
            (self._proc is not None) and 
            (not self._proc.poll())
        )

    def run(self, args: 'list'):
        if not self.is_running():
            self._args = args

            args = ' '.join(args)
            args = [self._path, args]

            self._proc = Popen(
                args=args,
                stdin=PIPE,
                stdout=PIPE,
                stderr=STDOUT,
            )

    def kill(self):
        if self.is_running():
            self._proc.send_signal(2)
            self._proc = None

    def restart(self):
        self.kill()
        self.run(self._args)


class TestbedControl:

    def __init__(
        self,
        testbed: 'TestbedModel',
    ):
        self._testbed = testbed
        self._buildTool: 'TestbedProcess' = None
        self._serialReader: 'TestbedProcess' = None
        self._rpcClient: 'TestbedProcess' = None

        self._setup()

    def _setup(self):
        self._buildTool = TestbedProcess(
            name='Testbed Build Tool',
            path='control/process/start_build_tool.sh'
        )

        self._serialReader = TestbedProcess(
            name='Testbed Serial Reader',
            path='control/process/start_serial_reader.sh'
        )

        self._rpcClient = TestbedProcess(
            name='Testbed RPC Client',
            path='control/process/start_rpc_client.sh'
        )

    def start_motes_firmware(self):
        ports = [m.port for m in self._testbed.motes]
        ports = ','.join(ports)

        if ports:
            hopseq = [str(h) for h in self._testbed.hopseq]
            hopseq = ','.join(self._testbed.hopseq)

            args = [
                '-f', 'all',
                '-u', ports
            ]

            args += ['-p', self._testbed.txPower] if self._testbed.txPower else []
            args += ['-i', self._testbed.txIntv] if self._testbed.txIntv else []
            args += ['-l', self._testbed.hopseqLen] if self._testbed.hopseqLen else []
            args += ['-h', hopseq] if hopseq else []

            self._buildTool.run(args)

    def stop_motes_firmware(self):
        ports = [m.port for m in self._testbed.motes]
        ports = ','.join(ports)

        args = [
            '-f', 'stopped',
            '-u', ports
        ]

        self._buildTool.run(args)

    def start_serial_reader(self):
        ports = [m.port for m in self._testbed.motes]
        ports = ','.join(ports)

        args = [
            '-t', self._testbed.name,
            '-p', ports
        ]

        self._serialReader.run(args)

    def stop_serial_reader(self):
        self._serialReader.kill()

    def start_rpc_client(self):
        args = [
            '-i', '60',
            '-r', 'analyze',
            '-g', 'all',
            '-t', self._testbed.name
        ]

        self._rpcClient.run(args)

    def stop_rpc_client(self):
        self._rpcClient.kill()

    def start_testbed(self, verbose=False):
        self.start_motes_firmware()

        if self._buildTool.is_running():
            retcode = self._buildTool._proc.wait()
            if verbose:
                if retcode == 0:
                    print('Firmware written to motes successfully.')
                else:
                    print('Error when trying to write firmware to motes.')

            if retcode == 0:
                self.start_serial_reader()
                if verbose:
                    print(f'start serial reader with '
                        f'PID {self._serialReader.pid}.')

                self.start_rpc_client()
                if verbose:
                    print(f'start analysis RPC client with '
                        f'PID {self._rpcClient.pid}.')
