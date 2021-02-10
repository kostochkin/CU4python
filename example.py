from examplelib import *

servers = Cu4ServersList(host_ip=HostIp())

for s in servers:
    for d in s.devices():
        d.init()
        print(d.data())
        if (d.__class__ == CU4DeviceTDM):
            print(d.thermometer_state())
            print(d.set_thermometer_on())
            print(d.thermometer_state())
            print(d.set_thermometer_off())
            print(d.thermometer_state())
            




