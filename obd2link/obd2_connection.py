import serial


class obd2_connection():
#    def __init__(self):
#        self.serial_connection = serial.Serial(
#            # assumes that you are hooked up to pi
#            port = '/dev/ttyUSB0',
#            baudrate = 115200,
#            parity = serial.PARITY_NONE,
#            stopbits = serial.STOPBITS_ONE,
#            bytesize = serial.EIGHTBITS,
#            rtscts = False,
#            dsrdtr = False,
#            xonxoff = False
#        )

    def obd2_connection(self, *args, **kwargs):


    def obd2_open(self):
        self.serial_connection.open()

    def obd2_close(self):
        self.serial_connection.close()

    def obd2_is_open(self):
        self.serial_connection.isOpen()