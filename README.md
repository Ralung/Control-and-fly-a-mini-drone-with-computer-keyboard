# Control-and-fly-a-mini-drone-with-computer-keyboard
In this project, I used a laptop and a 4-in-1 board to fly a mini drone by arrow keys.  
The advantages of this way are that it is not needed to modify the drone and original transmitter and it can also be copied by other drones quickly.  
I am really appreciate to goebish, multiprotocol project and pascallanger!  

![flowDiagram](https://user-images.githubusercontent.com/76200428/131668352-30f70dd4-786e-42e2-851b-ef6123f4ebba.jpg)

Contents:
  1. Flash the firmware of 4-in-1 module
  2. Set up a Python code  
    a. Binding process  
    b. Initial value adjustment and Remote controlling commands  

In this project, I used a E016H model from Eachine drone company and it used the protocol, "PROTO_E916HV2"

## 1. Flash the firmware of 4-in-1 module
#### Step 1.	 Download the Multiprotocol firmware flashing file
Please go to the following web address to download the firmware flashing file, and ensure the version is v1.3.1.92 or later.
https://github.com/pascallanger/DIY-Multiprotocol-TX-Module/releases/tag/v1.3.1.92

#### Step 2.	 Modifications of several files
There are four different files needed to be modified in this step, and these files can be found in the firmware flashing file downloaded in previous step.  
1.	Pins.h
    Please replace USART2_BASE with USART1_BASE in line 357 and line 358  
2.	Multiprotocol.ino  
    a.	Add “#define __arm__” in line 27.  
    ![2-a](https://user-images.githubusercontent.com/76200428/131667812-4cbe6405-1bbc-4fa5-be8c-9cc68c6f3289.jpg)  
    b.	Add “void __irq_usart1(void);” in line 66.  
    ![2-b](https://user-images.githubusercontent.com/76200428/131667914-c0230b1b-93b3-4206-8271-5327e3c53f22.jpg)  
    c.	Replace “usart2_begin” with “usart1_begin” in line 2110 and line 2117, replace “USART2_BASE” with “USART1_BASE” in line 2111 and line 2118, and comment out the line 2122.  
    ![2-c](https://user-images.githubusercontent.com/76200428/131667945-cdceb0ea-756d-4d3c-82b2-d8aa6ad20d53.jpg)  
    d.	Add the codes from line 2154 to line 2161 in the following picture.   
    ![2-d](https://user-images.githubusercontent.com/76200428/131667969-ea1df474-4016-47e5-95c5-a96704c1473d.jpg)  
    e.	Replace “USART2_BASE” with “USART1_BASE” in line 2212.  
    ![2-e](https://user-images.githubusercontent.com/76200428/131667992-1fda55af-6fe2-4b79-8fb1-d87f71c61bff.jpg)  
    f.	Replace “__irq_usart2” with “__irq_usart1” in line 2448.  
    ![2-f](https://user-images.githubusercontent.com/76200428/131668017-ed0d9da1-6645-4dd9-be78-1277baa65cc2.jpg)  
    g.	Replace “USART2_BASE” with “USART1_BASE” in line 2456, and there are to places needed to be modified in this line.  
    ![2-g](https://user-images.githubusercontent.com/76200428/131668044-9547e71f-71cf-480c-a97c-cef344c3d91b.jpg)  
 
3.	Multiprotocol.h  
Please change the protocol numbers of “PROTO_Q303” and “PROTO_E016HV2”, the original protocol number of former is 31 and it is in line 60；the original protocol number of the latter is 80 and it is in line 108.  
After modification, “PROTO_Q303” should have 80 as its new number and “PROTO_E016HV2” should have 31 as its new number.  
4.	Usart_f1.c  
In this file, please comment out the codes in line 203 to line 205. Please note that this file should be under the folder of Arduino IDE program files whose file path is depend on different computers.  
#### Step 3.  Flash firmware with Arduino IDE  
1.	Install the Multi 4-in1 STM32 Board in the Arduino IDE. In this paper, the version number is 1.2.1. [13]
2.	Get in the folder downloaded in step 1 and open “multiprotocol.ino” file in Arduino IDE. Choose the developing board as “4-in-1 STM32”, the Debug option as “no” and the USB support as “Disabled”. The COM port depends on user computer situation.
3.	Let Arduino IDE to compile the programs and upload to the 4-in-1 moduel.

## 2. Set up a Python code  
#### Step 1. Binding process  
Please use the file, "1drone_KBcontrol_Binding.py" to test whether the binding process is successful.  
Note:  
a. The file "stm32flash.exe" should be put with the Python file.  
b. Check the number of protocol is correct.  
c. Check the number of COM port is correct.  
d. Set all the "globals" as 1500 if it's the first try.  
e. The LED would flash fast if the 4-in-1 board starts its binding mode.  
e. In this step, the E016H drone would only start its propellers and get into ready mode for 20 seconds.  
d. Once the propellers are rotating, this step is over.  
#### Step 2. Initial value adjustment and Remote controlling commands
