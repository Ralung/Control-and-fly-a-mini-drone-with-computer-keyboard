# Control-and-fly-a-mini-drone-with-computer-keyboard
In this project, I used a laptop and a 4-in-1 board to fly a mini drone by arrow keys.
The advantages of this way are that it is not needed to modify the drone and original transmitter and it can also be copied by other drones quickly.
I am really appreciate to goebish, multiprotocol project and pascallanger!

Contents:
  1. Flash the firmware of 4-in-1 module
  2. Set up a Python code
    a. Binding process
    b. Initial value adjustment
    c. Remote controlling commands

In this project, I used a E016H model from Eachine drone company and it used the protocol, "PROTO_E916HV2"

##1. Flash the firmware of 4-in-1 module
####Step 1.	 Download the Multiprotocol firmware flashing file
Please go to the following web address to download the firmware flashing file, and ensure the version is v1.3.1.92 or later.
https://github.com/pascallanger/DIY-Multiprotocol-TX-Module/releases/tag/v1.3.1.92

####Step 2.	 Modifications of several files
There are four different files needed to be modified in this step, and these files can be found in the firmware flashing file downloaded in previous step.
**1.	Pins.h**
    Please replace USART2_BASE with USART1_BASE in line 357 and line 358
**2.	Multiprotocol.ino**
   a.	Add “#define __arm__” in line 27.
   b.	Add “void __irq_usart1(void);” in line 66.
   c.	Replace “usart2_begin” with “usart1_begin” in line 2110 and line 2117, replace “USART2_BASE” with “USART1_BASE” in line 2111 and line 2118, and comment out the line 2122.
   d.	Add the codes from line 2154 to line 2161 in the following picture. 
   e.	Replace “USART2_BASE” with “USART1_BASE” in line 2212.
   f.	Replace “__irq_usart2” with “__irq_usart1” in line 2448.
   g.	Replace “USART2_BASE” with “USART1_BASE” in line 2456, and there are to places needed to be modified in this line.
 
**3.	Multiprotocol.h**
Please change the protocol numbers of “PROTO_Q303” and “PROTO_E016HV2”, the original protocol number of former is 31 and it is in line 60；the original protocol number of the latter is 80 and it is in line 108.
After modification, “PROTO_Q303” should have 80 as its new number and “PROTO_E016HV2” should have 31 as its new number.
4.	Usart_f1.c
In this file, please comment out the codes in line 203 to line 205. Please note that this file should be under the folder of Arduino IDE program files whose file path is depend on different computers.
Step 3.  Flash firmware with Arduino IDE
1.	Install the Multi 4-in1 STM32 Board in the Arduino IDE. In this paper, the version number is 1.2.1. [13]
2.	Get in the folder downloaded in step 1 and open “multiprotocol.ino” file in Arduino IDE. Choose the developing board as “4-in-1 STM32”, the Debug option as “no” and the USB support as “Disabled”. The COM port depends on user computer situation.
3.	Let Arduino IDE to compile the programs and upload to the 4-in-1 moduel.

2. Set up a Python code
