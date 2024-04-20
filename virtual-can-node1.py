#!/usr/bin/env python

import can
import time
from random import shuffle
from Crypto.Cipher import AES
from statistics import mean

# My debug print statements and processes throughout are commented out. They can
# be uncommented easily for testing

# Define an easily changeable variable for whether or not to use encryption
ENC = True

# Define variables to use throughout
msgCnt = 0
data = []
dataBytes = b''
key = b'MakeThisKeySomethingUniqueToYou1'

# Define debugging variables
#recvMsgs = []
#encSentMsgs = []
#plnSentMsgs = []

# Define timing lists
msgSendTimes = []
msgRecvTimes = []

# Create a new CAN FD Bus Interface
bus = can.interface.Bus('vcan0', bustype='socketcan', bitrate=1000000, fd=True)

# Create a new AES Cipher. Assume key is already in byte format

# Build a standard 64-byte message
for num in [1,2,3,4,5,6,7,8]:
    for i in range(8):
        data.append(num)

# Blocking wait for the acknowledgement of first message
msg = bus.recv()

# Send a response to trigger the handshake to start the test
dataBytes = bytes(data)
send = can.Message(arbitration_id=456, is_extended_id=False, is_fd=True, data=dataBytes)
bus.send(send)

# Start the overall loop timer
total_tStart = time.perf_counter()

# Start message loop
while (msgCnt < 1001):

    # Start receiving timer
    recvStart = time.perf_counter()

    # Blocking wait for receiving message from other node
    msg = bus.recv()
    msg_data = msg.data

    # If using encryption, decrypt the message
    if ENC:
        aes_cipher = AES.new(key, AES.MODE_CTR, nonce=bytes(msgCnt%16))
        msg_data = aes_cipher.decrypt(msg.data)

    # Stop receiving timer
    recvStop = time.perf_counter()

    # Append message to received messages list
    #recvMsgs.append(msg_data)

    # Start sending timer
    sendStart = time.perf_counter()

    # Create a "response" message
    dataBytes = bytes(data)
    #plnSentMsgs.append(dataBytes)

    # If using encryption, encrypt the message
    if ENC:
        aes_cipher = AES.new(key, AES.MODE_CTR, nonce=bytes(msgCnt%16))
        dataBytes = aes_cipher.encrypt(dataBytes)

    # Craft and send the message
    send = can.Message(arbitration_id=456, is_extended_id=False, is_fd=True, data=dataBytes)
    bus.send(send)

    # Stop our send timer
    sendStop = time.perf_counter()

    # Store sent msgs for debug purposes
    #encSentMsgs.append(dataBytes)

    # Increment the overall message count
    msgCnt+=1

    # Shuffle the data before sending next
    shuffle(data)

    # Track timing data
    msgSendTimes.append(sendStop-sendStart)
    msgRecvTimes.append(recvStop-recvStart)

# Stop overall loop timer
total_tStop = time.perf_counter()

# Debug print the list of received messages
#for i in range(len(recvMsgs)):
#    print(recvMsgs[i])
#    print(encSentMsgs[i])
#    print(plnSentMsgs[i])
#    print()

# Print the timing statistics
print("Total Loop Time: {}".format(total_tStop - total_tStart))
print("Sending Times:")
print("\tAverage Time: {}".format(mean(msgSendTimes)))
print("\tMax Time: {}".format(max(msgSendTimes)))
print("\tMin Time: {}".format(min(msgSendTimes)))
print("Receiving Times:")
print("\tAverage Time: {}".format(mean(msgRecvTimes)))
print("\tMax Time: {}".format(max(msgRecvTimes)))
print("\tMin Time: {}".format(min(msgRecvTimes)))
