import serial
import time


class Obd2Connection():
    def __init__(self):
        self.parity = serial.PARITY_NONE
        self.stopbits = serial.STOPBITS_ONE
        self.bytesize = serial.EIGHTBITS
        self.rtscts = False
        self.dsrdtr = False
        self.xonxoff = False

    def get_port(self):
        #check the OS for FTDI USB Serial Device converter now attached to ttyUSB0
        print 'in get_port'

    def obd2_connection(self, *args, **kwargs):
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
        serial_connection.write(in_put + "\r\n")

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
