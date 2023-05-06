import subprocess


def get_sys_serial_devices() -> 'list[str]':
    devices = subprocess.run(
        ['ls /dev/ttyUSB*'],
        shell=True,
        capture_output=True
    )
    devices = devices.stdout.decode()
    devices = devices.split('\n')
    devices = devices[:len(devices) - 1]

    return devices
