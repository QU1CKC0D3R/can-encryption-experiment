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
aes_cipher = AES.new(key, AES.MODE_CTR)

# Build a standard 64-byte message
for num in [1,2,3,4,5,6,7,8]:
    for i in range(8):
        data.append(num)

# Send the initial message, but don't count this as part of the timer
dataBytes = bytes(data)
msg = can.Message(arbitration_id=123, is_extended_id=False, is_fd=True, data=dataBytes)
bus.send(msg)

# Once the message is sent, wait until a message is received
recv_msg = bus.recv()

# Start overall process timer
total_tStart = time.perf_counter()

# Initiate loop
while (msgCnt < 1001):

    # Craft and send a message to kick off 1000 message loop
    # Also start send timer
    sendStart = time.perf_counter()
    dataBytes = bytes(data)
    #plnSentMsgs.append(dataBytes)

    # Run encryption check and encrypt if required
    if ENC:
        aes_cipher = AES.new(key, AES.MODE_CTR, nonce=bytes(msgCnt%16))
        dataBytes = aes_cipher.encrypt(dataBytes)

    # Construct and send CAN FD message
    msg = can.Message(arbitration_id=123, is_extended_id=False, is_fd=True, data=dataBytes)
    bus.send(msg)

    # Stop send timer
    sendStop = time.perf_counter()

    # Wait to receive a reply (blocking) and start receive timer
    recvStart = time.perf_counter()
    recv_msg = bus.recv()
    recv_data = recv_msg.data

    # Run decryption on the message if required
    if ENC:
        aes_cipher = AES.new(key, AES.MODE_CTR, nonce=bytes(msgCnt%16))
        recv_data = aes_cipher.decrypt(recv_msg.data)

    # Stop receive timer
    recvStop = time.perf_counter()

    # Append the received message to output list to validate later
    #recvMsgs.append(recv_data)

    # Store sent msgs for debug purposes
    #encSentMsgs.append(dataBytes)

    # Incremement the message count
    msgCnt+=1

    # Shuffle the data to be sent -- slow but I think realistic
    shuffle(data)

    # Track timing data
    msgSendTimes.append(sendStop-sendStart)
    msgRecvTimes.append(recvStop-recvStart)

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
