# Purpose

The purpose of this repository is to provide a simple method for gauging what the impact of asymmetric encryption using AES would be on the CAN Bus protocol. This code is for a school experiment.

# Instructions

Instructions for how to run:

  * Setup the virtual can interface using the following commands:
     * `sudo modprobe vcan`
     * `sudo ip link add dev vcan0 type vcan`
     * `sudo ip link set up vcan0`
  * Start the first CAN node with the following command: `python3 virtual-can-node2.py`
  * Start the second CAN node with the following command: `python3 virtual-can-node2.py`

At this point, each node will complete and output some time metrics. You can then repeat tests as necessary, changing the `ENC` variable in both nodes to be `True` or `False` for Encryption or No Encryption respectively.
