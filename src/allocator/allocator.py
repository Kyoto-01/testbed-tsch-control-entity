from random import choice

from models import MoteModel
from utils.sys_info import get_sys_serial_devices


class TestbedResourceAllocator:

    @staticmethod
    def alloc_ports(
        count: 'int'
    ) -> 'list[str]':
        availablePorts = get_sys_serial_devices()[1::2]

        busyPorts = MoteModel.select_motes_by_busy(is_busy=True)
        busyPorts = [v.port for v in busyPorts.values()]

        allocated = []

        while (
            (len(allocated) < count) and 
            (len(availablePorts) > len(busyPorts))
        ):
            port = choice(availablePorts)

            if port not in busyPorts:
                mote = MoteModel(
                    port=port,
                    is_busy=True
                )

                allocated.append(port)
                busyPorts.append(port)

                MoteModel.insert_mote(mote)

        return allocated
