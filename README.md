odb2
====

stn1100-frpm.pdf
The OBDLink line of scan tools uses the STN11xx IC and is compatible with the ELM327 commands as well as the extended ST commands

#38400 baud (default) 

Working settings: with # http://www.furrysoft.de/?page=goserial
Speed/Baud: 115200 #http://theksmith.com/technology/hack-vehicle-bus-cheap-easy-part-1/
• 8 data bits 
• No parity bit 
• One stop bit 
• No handshaking 


Bus 001 Device 004: ID 0403:6001 Future Technology Devices International, Ltd FT232 USB-Serial (UART) IC

minicom -b 38400 -o -D /dev/ttyUSB0


virtualenv venv; source venv/bin/activate


dmesg | grep tty
usb 1-1.3: FTDI USB Serial Device converter now attached to ttyUSB0

ATI


Device ID 
Command Description 
DI Print device hardware ID string (e.g., “OBDLink r1.7”) 
I Print firmware ID string (e.g., “STN1100 v1.2.3”) 
MFR Print device manufacturer ID string 
SN Print device serial number 

USB:
http://www.raspberrypi.org/forums/viewtopic.php?f=28&t=70437

cyOBD-II
http://cyantific.de/raspberrypi/kw1281-live-diagnosis-with-raspberry-pi/

using Minicom
http://wolframpc.blogspot.ca/p/raspberry-pi-carputer-page-2.html

python 
http://techminor.blogspot.ca/2013/05/raspberry-pi-direct-usb-to-uart-using.html

http://obdcon.sourceforge.net/2010/06/obd-ii-pids/