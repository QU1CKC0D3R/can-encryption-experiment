# Purpose

The purpose of this repository is to provide a simple method for gauging what the impact of asymmetric encryption using AES would be on the CAN Bus protocol. This code is for a school experiment.

# Prerequisites

This functionality has only been tested on an Ubuntu 22.04 implementation with Python 3.10.12. You may need to modify commands to fit your needs.

To satisfy the required Python packages, simply run the following command:
`pip install -r requirements.txt`

# Instructions

Instructions for how to run:

  * Setup the virtual can interface using the following commands:
     * `sudo modprobe vcan`
     * `sudo ip link add dev vcan0 type vcan`
     * `sudo ip link set up vcan0`
  * Start the first CAN node with the following command: `python3 virtual-can-node2.py`
  * Start the second CAN node with the following command: `python3 virtual-can-node2.py`

At this point, each node will complete and output some time metrics. You can then repeat tests as necessary, changing the `ENC` variable in both nodes to be `True` or `False` for Encryption or No Encryption respectively.

Run the tests as many times as you like and collect results.
