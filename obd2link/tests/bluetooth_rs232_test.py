import time
import serial
import bluetooth


# MAC of my 00:04:3E:02:98:2B - OBDLink MX
bluetooth_mac = "00:04:3E:02:98:2B"
# Create the client socket
client_socket = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
#The linux command you can try is:
#rfcomm connect /dev/rfcomm0 XX:XX:XX:XX:XX:XX  1
#which means rfcomm connect <linux port> <MAC of the OBDLINK MX> <CHANNEL of the OBDLINK MX>
port = client_socket.connect((bluetooth_mac, 1))

print port
# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial(

    # assumes that you are hooked up to pi
    port=port,
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    rtscts=False,
    dsrdtr=False,
    xonxoff=False
)

ser.close()
ser.open()
ser.isOpen()

print 'Enter your commands below.\r\nInsert "exit" to leave the application.'

input=1
while 1 :
    # get keyboard input
    input = raw_input(">> ")
        # Python 3 users
        # input = input(">> ")
    if input == 'exit':
        ser.close()
        exit()
    else:
        # send the character to the device
        # (note that I happend a \r\n carriage return and line feed to the characters - this is requested by my device)
        ser.write(input + '\r\n')
        out = ''
        # let's wait one second before reading output (let's give device time to answer)
        time.sleep(1)
        while ser.inWaiting() > 0:
            out += ser.read(1)

        if out != '':
            print ">>" + out
