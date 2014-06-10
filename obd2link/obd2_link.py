import time
import os
import logging

import core.file_io as file_io
import core.dict_helper as dict_helper
import accelerometer.adxl345 as accelerometer
import obd2.obd2_connection as obd2_connection
from globals import application_properties
from globals import sensors


class Obd2Link():

    def __init__(self):

        #usb connection to mxlink
        self.connection = self.get_connection()

        # obd2 connection
        self.conn = obd2_connection.Obd2Connection()

        self.acc = accelerometer.ADXL345()
        self.ph = file_io.PropertiesHelper()
        self.dh = dict_helper.DictHelper()


    def get_connection(self):

        port = application_properties.get('input').get('port')
        baudrate = application_properties.get('input').get('baudrate')

        conn = obd2_connection.Obd2Connection()
        connection = conn.obd2_connection(port=port, baudrate=baudrate)

        return connection

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
                    print 'value of {0} after reading bus: {1}'.format(value, read)
                else:
                    print key, value

    def get_version(self):

        self.conn.obd2_close(self.connection)
        self.conn.obd2_open(self.connection)
        self.conn.obd2_is_open(self.connection)

        version_code = sensors.get('at').get('version')
        version2_code = sensors.get('at').get('version2')

        print version_code
        print version2_code

        self.conn.obd2_write(self.connection, 'ATI')
        read = self.conn.obd2_read(self.connection)

        if read == None:

            self.conn.obd2_write(self.connection, 'ATZ')
            read = self.conn.obd2_read(self.connection)
            print 'read after ATZ' + read

        print 'read after ATI: ' + read

    def make_human(self):
        self.conn.obd2_write(self.connection, 'ATL1')
        self.conn.obd2_write(self.connection, 'ATH1')
        self.conn.obd2_write(self.connection, 'ATS1')
        self.conn.obd2_write(self.connection, 'ATAL')
        #stream
        self.conn.obd2_write(self.connection, 'ATMA')

    def obd2_innitialize(self):


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
        self.dh.update_dict(self.temp_dict, 'x_acc', axes['x'])
        self.dh.update_dict(self.temp_dict, 'y_acc', axes['y'])
        self.dh.update_dict(self.temp_dict, 'z_acc', axes['z'])

        print "   x = %.3fG" % ( axes['x'] )
        print "   y = %.3fG" % ( axes['y'] )
        print "   z = %.3fG" % ( axes['z'] )

    def main(self):

        obd2_config_home = '/home/pi/obd2link/obd2link/config'

        application_properties_file = os.path.join(obd2_config_home, 'application.properties')
        application_properties = self.ph.get_yaml_config(filename=application_properties_file, use_full_path=True)

        sensors_file = os.path.join(obd2_config_home, 'codes.properties')
        sensors = self.ph.get_yaml_config(filename=sensors_file, use_full_path=True)

        logger_file = os.path.join(obd2_config_home, 'logger.properties')
        logger_config = self.ph.get_yaml_config(filename=logger_file, use_full_path=True)

        print application_properties
        print sensors
        print logger_config

        self.ph.set_logger(logger_config)
        logger = logging.getLogger("obd2")
        logger.info('testing_122')

        now = time.time()
        self.temp_dict = {'now': str(now)}

        self.get_version()
        self.make_human()
        #self.obd2_innitialize()
        #get_constants()
        #self.get_sensors()
        #self.get_acc_axes()


        #print self.temp_dict
        sorted_temp_dict = self.dh.sort_dict(self.temp_dict)
        #print sorted_temp_dict

        #TODO file name should be vin+epoc
        file_location = os.path.join(self.properties.get('output').get('data_output_folder'), 'soon_to_be_vin_{0}.csv'.format(now))
        self.ph.write_csv(sorted_temp_dict, file_location)


if __name__ == '__main__':
    Obd2Link().main()