import client2

import serial
import argparse

parser = argparse.ArgumentParser('Client for sending controller commands to a controller emulator')
parser.add_argument('port')
args = parser.parse_args()


c = client2.client2(port=args.port, baudrate=19200,timeout=1)

# Attempt to sync with the MCU
if not c.sync():
    print('Could not sync!')

if not c.send_cmd(c.BTN_A + c.DPAD_U_R + c.LSTICK_U + c.RSTICK_D_L):
    print('Packet Error!')

if not c.send_cmd(c.BTN_L + c.BTN_R):
    print('Packet Error!')

c.p_wait(0.05)
print ('sent')

if not c.send_cmd():
    print('Packet Error!')

c.testbench()

c.ser.close