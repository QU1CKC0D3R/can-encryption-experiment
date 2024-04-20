Instructions for how to run:

  * Setup the virtual can interface using the following commands:
     * `sudo modprobe vcan`
     * `sudo ip link add dev vcan0 type vcan`
     * `sudo ip link set up vcan0`
  * Start the first CAN node with the following command: `python3 virtual-can-node2.py`
  * Start the second CAN node with the following command: `python3 virtual-can-node2.py`
