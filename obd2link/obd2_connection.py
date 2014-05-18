import serial


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
            bautrate=self.baudrate,
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