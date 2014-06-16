import serial
import time
import platform


class Obd2Connection():
    def __init__(self):
        self.parity = serial.PARITY_NONE
        self.stopbits = serial.STOPBITS_ONE
        self.bytesize = serial.EIGHTBITS
        self.rtscts = False
        self.dsrdtr = False
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

    def obd2_connection(self, *args, **kwargs):

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

    def obd2_read(self, serial_connection):

        out_put = ''

       # let's wait one second before reading output (let's give device time to answer)
        time.sleep(0.1)
        while 1:
            char = serial_connection.read(1)
            if char == '\r' and len(out_put) > 0:
                break
            else:
                # if there is something in the buffer this will add it all up
                if (out_put != '' or char != '>') :
                    out_put = out_put + char
        return out_put
