import time
from datetime import datetime

import core.file_io as file_io
import core.dict_helper as dict_helper
import accelerometer.adxl345 as accelerometer
import obd2.obd2_connection as obd2_connection
import obd2.obd2_constants as obd2_constants


class Obd2Link():

    def __init__(self):

        #usb connection to mxlink
        self.connection = self.get_connection()

        # obd2 connection
        self.conn = obd2_connection.Obd2Connection()

        self.acc = accelerometer.ADXL345()
        self.ph = file_io.PropertiesHelper()
        self.dh = dict_helper.DictHelper()



        self.SENSORS = obd2_constants.SENSORS



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

        self.conn.obd2_close(self.connection)
        self.conn.obd2_open(self.connection)

        for key, value in self.SENSORS.items():
    #        print k, v
            for key, value in value.items():
                if key == 'hex':
                    self.conn.obd2_write(self.connection, value)
                    read = self.conn.obd2_read(self.connection)
                    self.temp_dict.update({value: read})
                    print 'after reading bus: ' + read
                else:
                    print key, value

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


        axes = self.acc.getAxes(True)
        self.ph.update_dict(self.temp_dict, 'acc_x', axes['x'])
        self.ph.update_dict(self.temp_dict, 'acc_y', axes['y'])
        self.ph.update_dict(self.temp_dict, 'acc_z', axes['z'])

        print "ADXL345 on address 0x%x:" % (self.acc.address)
        print "   x = %.3fG" % ( axes['x'] )
        print "   y = %.3fG" % ( axes['y'] )
        print "   z = %.3fG" % ( axes['z'] )

    def main(self):


        #this has to be moved to a global variable
        self.temp_dict = {'time stamp': str(datetime.now())}



        #get_version(connection)
        self.innitialize()
        #get_constants()
        self.get_sensors()
        self.get_acc_axes()


        self.temp_dict = self.dh.sort_dict(self.temp_dict)
        print self.temp_dict
        self.ph.write_csv(self.temp_dict)


if __name__ == '__main__':
    Obd2Link().main()