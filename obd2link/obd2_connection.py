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

        count = 0
        serial_connection.open()

        # initialize
        self.obd2_write("atz")

        #echo off
        self.obd2_write("ate0")
        self.obd2_write("0100")
        ready = self.obd2_read()

        print "what is ready looking like today?" + ready

        if ready == "BUSINIT: ...OK":
            ready = self.obd2_read()
            print "0100 response2: " + ready
            return None
        else:
            #ready=ready[-5:] #Expecting error message: BUSINIT:.ERROR (parse last 5 chars)
            time.sleep(5)
            if count == 5:
                ready = self.obd2_read()
                print "0100 response2: " + ready + " closing time"
                self.obd2_close()
                return None
            else:
                count = count + 1


    def obd2_close(self, serial_connection):
        serial_connection.close()

    def obd2_is_open(self, serial_connection):
        serial_connection.isOpen()

    def obd2_write(self, serial_connection, in_put):

        serial_connection.flushOutput()
        serial_connection.flushInput()
        serial_connection.write(in_put + '\r\n')

    def obd2_read(self, serial_connection):

        out_put = ''

       # let's wait one second before reading output (let's give device time to answer)
        time.sleep(1)
        while serial_connection.inWaiting() > 0:
            out_put += serial_connection.read(1)

        if out_put != '':
            return out_put
        else:
            return 'no output' # put exception in here

