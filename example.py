from cu4lib.server import *
from cu4lib.simplelog import StdioLogger

import cu4lib.devices.td.m0 as m
import cu4lib.devices.sd.m0 as sspd

servers = Cu4ServersList(host_ip=HostIp(), logger=StdioLogger(take=32))

print(servers)

for s in servers:
    if s.ip().value != "192.168.255.202":
        continue

    for d in s.modules:
        if (d.__class__ == sspd.CU4SDM0):
            d.init()
            # Autorecovery test
            print(d.auto_recovery.counts)
            d.auto_recovery.reset_counts()
            d.auto_recovery.enabled = not d.auto_recovery.enabled
            print(d.auto_recovery.enabled)
            d.auto_recovery.timeout += 1
            print(d.auto_recovery.timeout)
            d.auto_recovery.threshold += 1
            print(d.auto_recovery.threshold)
            d.auto_recovery.threshold += 1
            print(d.auto_recovery.threshold)
            # bias tests
            d.bias.current += 1
            print(d.bias.current)
            print(d.bias.voltage)
            # counter tests
            d.counter.enabled = not d.counter.enabled
            print(d.counter.enabled)
            print(d.counter.counts)
            d.counter.time_constant += 1
            print(d.counter.time_constant)
            # bias tests
            d.bias.current += 1
            print(d.bias.current)
            print(d.bias.voltage)
            # comparator tests
            d.comparator.enabled = not d.comparator.enabled
            print(d.comparator.enabled)
            d.comparator.level += 1
            print(d.comparator.level)
        if (d.__class__ == CU4TDM0):
            d.init()
            # thermometer tests
            d.thermometer.enabled = not d.thermometer.enabled
            print(d.thermometer.enabled)
            print(d.thermometer.temperature)
            # thermometr.bias tests
            d.thermometer.bias.current += d.thermometer.bias.current
            print(d.thermometer.bias.current)
            print(d.thermometer.bias.voltage)
            # pressure meter tests
            print(d.pressure_meter.pressure)
            print(d.pressure_meter.voltage.positive)
            print(d.pressure_meter.voltage.negative)

