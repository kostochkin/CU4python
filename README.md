# cu4python

A Python library for modular electronic system Control Unit 4 by Scontel.

## Requirements

Python 2.7 and higher

## Installation

    $ git clone https://github.com/kostochkin/cu4python
    $ cd cu4python

With pip:

    $ pip install .

With easy-install:

    $ sudo easy_install .

Or:

    $ python setup.py build
    $ sudo python setup.py install

## Module classes


These classes representing available CU4 modules are:

- class CU4TDM0
- class CU4TDM1
- class CU4SDM0
- class CU4SDM1

They provide API to corresponding hardware modules.
Note that sometimes data may be lost in transition. In this case the value of a property will be None.

Each class has own docstrings. Use help() function to get description of these classes.

### Examples

    > import CU4lib as cu
    > help(cu.CU4TDM0)

## Auxiliary Classes

This library contains several auxiliary classes:

### class HostIp

This class encapsulates IP address of any host. It also helps to determine IP address of client.

#### Example:

    > import CU4lib as cu
	> ip1 = cu.HostIp()
	> print(ip.value)
 	.....
	> ip2 = cu.HostIp("127.0.0.1")
	> print(ip.value)
	.....

### class CU4ServersList

This class inteded to find the Control Unit on local network.

#### Example

    import CU4lib as cu

    for unit in cu.CU4List(host_ip=cu.HostIp()):
        print(unit)
        for module in unit:
            print(module)

# References

* CU4lib doc: http://rplab.ru/~kostochkin/scontel/cu4lib.pdf
* test/example.py
* Manuals: https://www.scontel.ru/index/manuals/
* SCPI interface: https://www.scontel.ru/wp-content/uploads/2020/08/Commands-CU.pdf
* Scontel site: https://www.scontel.ru

