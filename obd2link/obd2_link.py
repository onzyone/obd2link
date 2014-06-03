import time
from datetime import datetime

import core.file_io as file_io
import core.dict_helper as dict_helper
import accelerometer.adxl345 as accelerometer
import obd2.obd2_connection as obd2_connection
import obd2.obd2_constants as obd2_constants


class Obd2Link():

    def __init__(self):
        self.connection = self.get_connection()
        self.conn = obd2_connection.Obd2Connection()
        self.ph = file_io.PropertiesHelper()
        self.dh = dict_helper.DictHelper()

    def get_connection(self):

    # this will need to be taken care of by a get call later on
        port = '/dev/ttyUSB0'
        baudrate = 115200

        conn = obd2_connection.Obd2Connection()
        connection = conn.obd2_connection(port=port, baudrate=baudrate)

        return connection

    def get_constants(self):
        constants = obd2_constants.CONSTANTS
        for key, value in constants.items():
            print key, value

    def get_sensors(self):

        temp_dict = {'time stamp': str(datetime.now())}

        self.conn.obd2_close(self.connection)
        self.conn.obd2_open(self.connection)

        sensors = obd2_constants.SENSORS

        for key, value in sensors.items():
    #        print k, v
            for key, value in value.items():
                if key == 'hex':
                    self.conn.obd2_write(self.connection, value)
                    read = self.conn.obd2_read(self.connection)
                    temp_dict.update({value: read})
                    print 'after reading bus: ' + read
                else:
                    print key, value


        self.dh.sort_dict(temp_dict)
        print temp_dict

        self.ph.write_csv(temp_dict)

    def get_version(self):

        self.conn.obd2_close(self.connection)
        self.conn.obd2_open(self.connection)
        self.conn.obd2_is_open(self.connection)

        self.conn.obd2_write(self.connection, 'ATI')
        read = self.conn.obd2_read(self.connection)

        print 'read after ATI: ' + read

    def innitialize(self):


        # this is still in prototype stage too.
        count = 0

        self.conn.obd2_close(self.connection)
        self.conn.obd2_open(self.connection)

        self.conn.obd2_write(self.connection, 'ATZ')
        read = self.conn.obd2_read(self.connection)

        print 'read after ATZ: ' + read

        time.sleep(5)

        #echo off
        self.conn.obd2_write(self.connection, 'ATE0')
        read = self.conn.obd2_read(self.connection)

        print 'read after ATE0: ' + read

        self.conn.obd2_write(self.connection, 'ATDP')
        read = self.conn.obd2_read(self.connection)

        print 'read after ATDP: ' + read

        #not connected: UNABLE TO CONNECTSEARCHING


        #Sensor("          Supported PIDs", "0100", hex_to_bitstring  ,""       ),
        self.conn.obd2_write(self.connection, '0100')
        read = self.conn.obd2_read(self.connection)
        print 'read after 0100: ' + read

        #Sensor("     Coolant Temperature", "0105", temp              ,"C"      ),
        self.conn.obd2_write(self.connection, '0105')
        read = self.conn.obd2_read(self.connection)
        # expected output: hex, 41 05 79
        # where 41 05 is the header and 79 is the hex value
        print 'read after 0105: ' + read

    def get_acc_axes(self):

        acc = accelerometer.ADXL345()
        axes = acc.getAxes(True)

        print "ADXL345 on address 0x%x:" % (acc.address)
        print "   x = %.3fG" % ( axes['x'] )
        print "   y = %.3fG" % ( axes['y'] )
        print "   z = %.3fG" % ( axes['z'] )

    def main(self):

        #get_version(connection)
        self.innitialize()
        #get_constants()
        self.get_sensors()
        self.get_acc_axes()

if __name__ == '__main__':
    Obd2Link().main()