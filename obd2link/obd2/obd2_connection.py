import serial
import platform


class Obd2Connection():
    def __init__(self):
        self.parity = serial.PARITY_NONE
        self.stopbits = serial.STOPBITS_ONE
        self.bytesize = serial.EIGHTBITS
        #was False, testing
        self.rtscts = True
        #was False, testing
        self.dsrdtr = True
        self.xonxoff = False

    def get_port(self):
        # code was taken from the pyobd project: http://sourceforge.net/projects/pyobd2/
        """scan for available ports. return a list of serial names"""
        available = []
        for i in range(256):
            try: #scan standart ttyS*
                s = serial.Serial(i)
                available.append(s.portstr)
                s.close()   # explicit close 'cause of delayed GC in java
            except serial.SerialException:
                pass
        for i in range(256):
            try: #scan USB ttyACM
                s = serial.Serial("/dev/ttyACM" + str(i))
                available.append(s.portstr)
                s.close()   # explicit close 'cause of delayed GC in java
            except serial.SerialException:
                pass
        for i in range(256):
            try:
                s = serial.Serial("/dev/ttyUSB" + str(i))
                available.append(s.portstr)
                s.close()   # explicit close 'cause of delayed GC in java
            except serial.SerialException:
                pass
        for i in range(256):
            try:
                s = serial.Serial("/dev/ttyd" + str(i))
                available.append(s.portstr)
                s.close()   # explicit close 'cause of delayed GC in java
            except serial.SerialException:
                pass

        # ELM-USB shows up as /dev/tty.usbmodemXXXX, where XXXX is a changing hex string
        # on connection; so we have to search through all 64K options
        if len(platform.mac_ver()[0]) != 0:  #search only on MAC
            for i in range(65535):
                extension = hex(i).replace("0x", "", 1)
                try:
                    s = serial.Serial("/dev/tty.usbmodem" + extension)
                    available.append(s.portstr)
                    s.close()
                except serial.SerialException:
                    pass

        return available

    def obd2_usb_connection(self, *args, **kwargs):

        #get ports
#        port_names = self.get_port()
#        for port in port_names:
#            print port

        # this will be replaced by the code above ... when it is working
        self.port = kwargs.pop('port')
        self.baudrate = kwargs.pop('baudrate')
#        self.parity = kwargs.iteritems('parity')

        self.serial_connection = serial.Serial(
            port=self.port,
            baudrate=self.baudrate,
            parity=self.parity,
            stopbits=self.stopbits,
            bytesize=self.bytesize,
            rtscts=self.rtscts,
            dsrdtr=self.dsrdtr,
            xonxoff=self.xonxoff
        )

        return self.serial_connection

    def obd2_bluetooth_connection(self, **kwargs):

        import bluetooth

        self.bluetooth_mac = kwargs.pop('bluetooth_mac')
        # Create the client socket
        client_socket = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
        bluetooth_connection = client_socket.connect((self.bluetooth_mac, 1))

        return bluetooth_connection

        #The linux command you can try is:
        #rfcomm connect /dev/rfcomm0 XX:XX:XX:XX:XX:XX  1
        #which means rfcomm connect <linux port> <MAC of the OBDLINK MX> <CHANNEL of the OBDLINK MX>


    def obd2_open(self, serial_connection):
        serial_connection.open()

    def obd2_close(self, serial_connection):
        serial_connection.close()

    def obd2_is_open(self, serial_connection):
        serial_connection.isOpen()

    def obd2_write(self, serial_connection, in_put):

        serial_connection.flushOutput()
        serial_connection.flushInput()
        for c in str(in_put):
            serial_connection.write(c)
        serial_connection.write("\r\n")

    def obd2_read_raw(self, serial_connection):

        buffer = ""

        while serial_connection.inWaiting() > 0:
            buffer += serial_connection.read(1)

        return buffer

    def obd2_read(self, serial_connection):

        buffer = ""
        repeat_count = 0

       # let's wait one second before reading output (let's give device time to answer)
        while 1:
            c = serial_connection.read(1)
            if len(c) == 0:
                if (repeat_count == 5):
                    break
                print "Got nothing\n"
                repeat_count = repeat_count + 1
                continue

            if c == '\r' and len(c) > 0:
                break

            #if something is in buffer, add everything
            elif buffer != "" or c != ">":
                buffer = buffer + c

        if (buffer == ""):
            return None

        return buffer

#        time.sleep(0.1)
#        while 1:
#            char = serial_connection.read(1)
#            if char == '\r' and len(out_put) > 0:
#                break
#            else:
#                # if there is something in the buffer this will add it all up
#                if (out_put != '' or char != '>') :
#                    out_put = out_put + char
#        return out_put
