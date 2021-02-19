from cu4lib.server import *
from cu4lib.simplelog import StdioLogger
from cu4lib.devices.components.descriptors import CU4ValueError

import cu4lib.devices.td.m0 as m
import cu4lib.devices.sd.m0 as sspd

servers = Cu4ServersList(host_ip=HostIp(), logger=StdioLogger(take=32))

print(servers)

for s in servers:
    if s.ip().value != "192.168.255.202":
        continue
    
    print(s.modules)

    for d in s.modules:
        if (d.__class__ == sspd.CU4SDM0):
            d.init()
            print(d.data)
            # Autorecovery test
            print(d.auto_recovery.counts)
            d.auto_recovery.reset_counts()
            d.auto_recovery.enabled = not d.auto_recovery.enabled
            print(d.auto_recovery.enabled)
            d.auto_recovery.timeout += 1.1
            print(d.auto_recovery.timeout)
            d.auto_recovery.threshold += 1.1
            print(d.auto_recovery.threshold)
            # bias tests
            d.bias.current += 1.1
            print(d.bias.current)
            print(d.bias.voltage)
            try:
                d.bias.voltage = 5
            except CU4ValueError:
                print("r/o checked")
            # counter tests
            d.counter.enabled = not d.counter.enabled
            print(d.counter.enabled)
            print(d.counter.counts)
            try:
                d.counter.counts = 5
            except CU4ValueError:
                print("r/o checked")
            d.counter.time_constant += 1.1
            print(d.counter.time_constant)
            # bias tests
            d.bias.current += 1.1
            print(d.bias.current)
            print(d.bias.voltage)
            try:
                d.bias.voltage = 5
            except CU4ValueError:
                print("r/o checked")
            # comparator tests
            d.comparator.enabled = not d.comparator.enabled
            print(d.comparator.enabled)
            d.comparator.level += 1.1
            print(d.comparator.level)
            # amplifier tests
            d.amplifier.enabled = not d.amplifier.enabled
            print(d.amplifier.enabled)
            if d.is_cmp:
                d.switch_to_amp_out()
                print(d.is_cmp)
                d.switch_to_cmp_out()
                print(d.is_cmp)
            else:
                d.switch_to_cmp_out()
                print(d.is_cmp)
                d.switch_to_amp_out()
                print(d.is_cmp)
            d.shorted = not d.shorted
            print(d.shorted)
        if (d.__class__ == CU4TDM0):
            d.init()
            print(d.data)
            # thermometer tests
            d.thermometer.enabled = not d.thermometer.enabled
            print(d.thermometer.enabled)
            print(d.thermometer.temperature)
            try:
                d.thermometer.temperature = 5.1
            except CU4ValueError:
                print("r/o checked")
            # thermometr.bias tests
            d.thermometer.bias.current += d.thermometer.bias.current
            print(d.thermometer.bias.current)
            print(d.thermometer.bias.voltage)
            try:
                d.thermometer.bias.voltage = 5
            except CU4ValueError:
                print("r/o checked")
            # pressure meter tests
            print(d.pressure_meter.pressure)
            try:
                d.pressure_meter.pressure = 5
            except CU4ValueError:
                print("r/o checked")
            print(d.pressure_meter.voltage.positive)
            try:
                d.pressure_meter.voltage.positive = 5
            except CU4ValueError:
                print("r/o checked")
            print(d.pressure_meter.voltage.negative)
            try:
                d.pressure_meter.voltage.negative = 5
            except CU4ValueError:
                print("r/o checked")
