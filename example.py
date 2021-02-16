from cu4lib.server import *
from cu4lib.simplelog import StdioLogger

from cu4lib.devices.cu4device import CU4Device
import cu4lib.devices.temperature_drivers as td
import cu4lib.devices.td.types as tdm

servers = Cu4ServersList(host_ip=HostIp(), logger=StdioLogger(take=32))

# help(td.CU4DeviceTDMConstant)

for s in servers:
    if s.ip().value != "192.168.255.202":
        continue
    
    print(s.modules)

    for d in s.modules:
        if (d.__class__ == CU4DeviceTDM0):
            d.init()
            d.thermometer.enabled
            d.thermometer.enabled = True
            d.thermometer.enabled
            d.thermometer.enabled = False
            d.thermometer.enabled
            d.thermometer.enabled = True
            d.thermometer.temperature
            d.thermometer.bias.current
            d.thermometer.bias.voltage
            d.thermometer.bias.current = 1.5
            d.thermometer.bias.current
            d.thermometer.bias.voltage
            d.pressure_meter.pressure
            d.pressure_meter.voltage.positive
            d.pressure_meter.voltage.negative
            print(d.constants.current_adc.slope)
            d.constants.current_adc.slope = 100
            print(d.constants.current_adc.slope)
            d.constants.current_adc.slope = 1
            print(d.constants.current_adc.slope)
            print(d.constants.current_adc.intercept)
            d.constants.current_adc.intercept = 100
            print(d.constants.current_adc.intercept)
            d.constants.current_adc.intercept = 0
            print(d.constants.current_adc.intercept)
            a = d.constants.pressure_voltage_n_adc.copy()
            a.slope = 100
            d.constants.pressure_voltage_n_adc = a
            a = d.constants.current_dac.copy()
            a.intercept = 123
            d.constants.current_dac = a
            print(d.constants.pressure_voltage_n_adc)
            print(d.constants.pressure_voltage_n_adc.copy())
            print(d.constants)
            print(d.constants.copy())
            d._get_json("PRSC?")
            print(list(d.temperature_table))
            print(d.temperature_table.copy().dict())
            print(d.data())
            d.thermometer.enabled = False
            print(d.data().commutator_on)
            print(d.data())
            d.temperature_table = tdm.TemperatureTableCopy([tdm.TemperaturePoint((3*x,x/100)) for x in range(1,101)])
            print(d.temperature_table.copy().dict())
            

