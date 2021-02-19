# cu4python

A Python 3 library for modular electronic system Control Unit 4 by Scontel.

## Module classes

These classes representing available modules are:

- class CU4TDM0
- class CU4TDM1
- class CU4SDM0

Each class has own docstrings. Use help() function to get description of these classes.

### Example

    > import CU4lib as cu
    > help(cu.CU4TDM0)

## Auxiliary Classes

This library contains several auxiliary classes:

### class HostIp

This class encapsulates Ip address of any host. It also helps determines Ip address of client.

#### Example:

    > import CU4lib as cu
	> ip1 = cu.HostIp()
	> print(ip.value)
 	.....
	> ip2 = cu.HostIp("127.0.0.1")
	> print(ip.value)
	.....

### class Cu4ServersList

This class inteded to find the Control Unit on local network.

#### Example

    for server in Cu4ServersList(host_ip=HostIp()):
        print(server)
        for module in server:
            print(module)


# References

* cu4lib/test/example.py
* Manuals: https://www.scontel.ru/index/manuals/
* SCPI interface: https://www.scontel.ru/wp-content/uploads/2020/08/Commands-CU.pdf
* Scontel site: https://www.scontel.ru

