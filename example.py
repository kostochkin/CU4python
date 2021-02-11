from cu4lib.server import *

from cu4lib.devices.cu4device import CU4Device

servers = Cu4ServersList(host_ip=HostIp())

for s in servers:
    for d in s.devices():
        d.init()
        print(d.data())
        if (d.__class__ == CU4DeviceTDM):
            print(d.thermometer.enabled)
            d.thermometer.enabled = True
            print(d.thermometer.enabled)
            d.thermometer.enabled = False
            print(d.thermometer.enabled)
            d.thermometer.enabled = True
            print(d.thermometer.enabled)
            print(d.thermometer.temp)
            print(d.thermometer.bias.curr)
            print(d.thermometer.bias.volt)
            d.thermometer.bias.curr = 1.5
            print(d.thermometer.bias.curr)
            print(d.thermometer.bias.volt)
            print(d.pressure_meter.pres)
            




