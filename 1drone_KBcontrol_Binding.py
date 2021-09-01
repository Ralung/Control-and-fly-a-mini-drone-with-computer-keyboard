################################
################################
import serial  # pip3 install pyserial
import time
import os
import msvcrt
import cv2
import keyboard

### protocol constants
E016HV2 = 31

##############
### settings ####
##############
protocol = E016HV2  # select protocol according to the receiver series (V/D/X)
COM_PORT = 'COM5'  # the COM port the JP4in1 is connected to, eg '/dev/ttyUSB0'
# select stm32flash executable, it must be copied along this file
STM32FLASH = 'stm32flash.exe'
#STM32FLASH = 'stm32flash_osx'
#STM32FLASH = 'stm32flash_linux32'
#STM32FLASH = 'stm32flash_linux64'

### end of settings


### more constants
AILERON = 0  # channel 1
ELEVATOR = 1
THROTTLE = 2
RUDDER = 3
CHANNEL5 = 4
CHANNEL6   = 5
CHANNEL7 = 6
CHANNEL8 = 7  # channel 8

# This is like fine tunning on OpenTx transmitter
option_protocol = 167 
###


### globals
A = 1560 #1540
E = 1750 #1490
T = 1400 #1375
R = 1505 #1490
serial_handle = False
channels = [A, E, T, R, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500]
packed_channels = bytearray([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
###


### utilities
def us_to_multi(us):
    # convert servo pwm value to multi value
    if us < 860:
        us = 860
    elif us > 2140:
        us = 2140
    result = int(((us-860)<<3)/5)    
    if result < 2047:
        return result
    else:
        return 2047
    
def pack_channels():
    # pack 16 channels into a 22 byte array (16 x 11bit)
    global packed_channels
    bits = 0
    bitsavailable = 0
    idx = 0
    for ch in range(16):
        val = us_to_multi(channels[ch])
        bits |= val << bitsavailable;
        bitsavailable += 11;
        while bitsavailable >= 8:
            packed_channels[idx] = bits & 0xff
            bits >>= 8
            bitsavailable -= 8;
            idx += 1
###


### module control functions        
def start_module():
    # start JP4in1 firmware while in BOOT0 mode, let stm32flash do its magic
    # we have to do that when the JP4in1 is started from USB since it has an
    # hardwired connection to BOOT0, preventing it to boot the firmware automatically
    global serial_handle
    command = "{} -g 0x8002000 {}".format(STM32FLASH, COM_PORT)
    print("starting JP4in1 firmware")
    print(command)
    try:
        res = os.system(command)
    except:
        print("couldn't run {}".format(STM32FLASH))
        return False
    if res != 0:
        print("stm32flash failed, if the JP4in1 firmware is already running (red LED flashing), just ignore this message")
        print("- is the JP4in1 module connected to the computer ?")
        print("- has the module been flashed with the proper firmware ?")
        print("- is a CP210x USB bridge driver installed ?")
        print("- is the module mapped to the proper COM_PORT ? ({})".format(COM_PORT))
        print("- is STM32FLASH command set properly for this OS ?")
        print("- have you tried turning the JP4in1 module on & off ?\n")
    else:
        print("Multi-Module is running")
    print ("opening {} @ 50000 8E2".format(COM_PORT))
    try:
        serial_handle = serial.Serial(COM_PORT, 50000, serial.EIGHTBITS, serial.PARITY_EVEN, serial.STOPBITS_TWO)
    except:
        print("error opening COM port")
        return False
    print("module waiting for commands")
    return True

def send_bind_packets(timeout):
    # send bind packets for x seconds, several receivers can be bound simultaneously
    header = bytearray([0x55, protocol, 0x00, option_protocol ])
    stoptime = time.time()+timeout
    # start by sending a dummy protocol change to the module
    # since it cannot enter bind state otherwise
    for loop in range(10):
        serial_handle.write(bytearray([0x55, protocol, 0x00, option_protocol, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]))
        time.sleep(0.05)
    print("sending bind packets for {} seconds".format(timeout))
    while time.time() < stoptime: 
        pack_channels()
        packet = (header + packed_channels)
        serial_handle.write(packet)
        time.sleep(0.05)
    
def send_control_packet():
    # this function must be called at least once every 70ms
    # or the module will switch to failsafe mode
    header = bytearray([0x55, protocol, 0x00, option_protocol])
    pack_channels()
    #packed_channels = bytearray([128,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
    packet = (header + packed_channels)
    serial_handle.write(packet)
    
def send_failsafe_packet():
    # set failsafe mode to "no pulse"
    for loop in range(10):
        serial_handle.write(bytearray([0x55, protocol, 0x00, option_protocol, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]))
        time.sleep(0.05)

def takeoff(channel, parameter):
    channels[channel] = parameter
    send_control_packet()
    time.sleep(0.01)
    for q in range(50):
        parameter += 15
        channels[channel] = parameter
        send_control_packet()
        time.sleep(0.01)

    time.sleep(0.03)
    for q in range(50):
        parameter -= 15
        channels[channel] = parameter
        send_control_packet()
        time.sleep(0.01)

def hovering():
    channels[THROTTLE] = T
    send_control_packet()
    time.sleep(0.02)

##################
### main program
##################

if __name__ == "__main__":
    # start JP4in1 module and open COM port
    if not start_module():
        print("couldn't start JP4in1 module, exiting ...")
        exit(1)
    
    send_bind_packets(5)
    print("bind completed")
    send_failsafe_packet()    
    print("starting channels transmition")
       
    channels[THROTTLE] = T
    print("Intialize THROTTLE value")
    send_control_packet()
    time.sleep(0.02)
    print("Start, press CTRL+C to stop!")

    takeoff(THROTTLE, T)
    
## This function must be called at least once every 70ms
    while 1:
        hovering()
        print(" Hovering ")
        
        print(" else, A = ", channels[AILERON], " E = ", channels[ELEVATOR], " T = ",  channels[THROTTLE], " R = ", channels[RUDDER])
        print("A=", A, "E=", E, "T=", T,"R=",R)
##        send packet to JP4in1 module
##        send_control_packet()
##        need a short pause between packets
##        time.sleep(0.01)
        
