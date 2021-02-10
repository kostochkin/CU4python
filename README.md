# cu4python

An example of communication with CU4 using Python.

There are two files: example.py and examplelib.py

# examplelib.py

This file contains several classes showing main use cases:

* HostIP encapsulates IP address and helps determine IP address of the client
* Cu4ServersList shows an example how to find server containing devices
* CU4Server shows an example how to enumerate devices on server
* CU4Device shows an example how to send general SCPI commands
* CU4DeviceSDM and CU4DeviceTDM show an example how to send devices commands

Note that this is not a complete library.

# example.py

This script shows an example how classes work together.
It creates Cu4ServersList instance. Then it run simple script for each device on each server:
- It initializes the device
- It gets data from the device
- If device is thermometer it does useless example work.

# See also

* Manuals: see https://www.scontel.ru/index/manuals/
* SCPI interface: https://www.scontel.ru/wp-content/uploads/2020/08/Commands-CU.pdf
* Scontel site: see https://www.scontel.ru



