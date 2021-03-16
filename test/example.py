from CU4lib.servers import *
from CU4lib.simplelog import StdioLogger
from CU4lib.devices.components.descriptors import CU4ValueError

from CU4lib import *

# preparing test server

servers = CU4List(logger=StdioLogger())

s = servers["127.0.0.1"]
#s.add_modules([0, 1, 2])

# end of preparing

# broken server

from .mockbrokenserver import BrokenCU4Server

#brokenserv = BrokenCU4Server(HostIp("127.0.0.1"), logger=StdioLogger())
#brokenserv.set_probability(0.7937)
#cu4mess = CU4Messenger(SCPI(brokenserv), attempts=3)
#gen = CU4CommandMessenger(GEN() & DEV(0), cu4mess)
#dev = CU4CommandMessenger(DEVT("CU4TDM0") & DEV(0), cu4mess)
#tdm0 = CU4TDM1(gen, dev, 0)
#
#fails = 0
#trues = 0
#
#for x in range(10):
#    tdm0.data
#    if tdm0.action_failed:
#        fails += 1
#    else:
#        trues += 1
#
#print(abs(fails - trues))
#print(abs(fails - trues) < 50)
#
# end of broken server

for x in range(0, 1):
    servers = CU4List(logger=StdioLogger())
    print(s.modules)
    for d in s.modules:
        d.init()
        print(d.id)
        print(d.last_error)
        if (d.__class__ == CU4SDM1 or d.__class__ == CU4SDM0):
            # Autorecovery test
            print(d.data)
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
            # thermometer tests
            print(d.data)
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
        if (d.__class__ == CU4TDM1):
            d.current = 5
            d.thermometer1.current = 1
            print(d.thermometer1.temperature)
            print(d.thermometer1.voltage)
            d.thermometer2.current = 2
            print(d.thermometer2.temperature)
            print(d.thermometer2.voltage)
            d.thermometer3.current = 3
            print(d.thermometer3.temperature)
            print(d.thermometer3.voltage)
            d.thermometer4.current = 4
            print(d.thermometer4.temperature)
            print(d.thermometer4.voltage)
            print(d.enabled_5v)
            print(d.enabled_25v)
            d.enabled_5v = not d.enabled_5v
            d.enabled_25v = not d.enabled_25v
            print(d.enabled_5v)
            print(d.enabled_25v)
            print(d.voltages)
            print(d.temperatures)
            print(d.switch_mode)
            d.switch_ac()
            print(d.switch_mode)
            d.switch_connect()
            print(d.switch_mode)
            d.switch_disconnect()
