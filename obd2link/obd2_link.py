import time
import os
import logging

import core.file_io as file_io
import core.dict_helper as dict_helper
import core.globals as globals
import core.converters as converters

import accelerometer.adxl345 as accelerometer
import obd2.obd2_connection as obd2_connection
import lcd.ssd1306 as lcd


class Obd2Link():

    def __init__(self):

        self.application_properties, self.sensors, self.logger_config = globals.get_globals()

        self.sample_rate = self.application_properties.get('input').get('sample_rate')
        self.number_of_loops = self.application_properties.get('input').get('number_of_loops')

        #usb connection to mxlink
        self.connection = self.get_connection()

        # obd2 connection
        self.conn = obd2_connection.Obd2Connection()

        #self.acc = accelerometer.ADXL345()
        self.ph = file_io.PropertiesHelper()
        self.dh = dict_helper.DictHelper()


    def get_connection(self):

        port = self.application_properties.get('input').get('port')
        baudrate = self.application_properties.get('input').get('baudrate')

        conn = obd2_connection.Obd2Connection()
        connection = conn.obd2_connection(port=port, baudrate=baudrate)

        return connection

    def open_close(self):
        self.conn.obd2_close(self.connection)
        self.conn.obd2_open(self.connection)
        self.conn.obd2_is_open(self.connection)

    def get_vin(self):


        print 'getting_vin'

        #echo off
        self.conn.obd2_write(self.connection, 'ATZ')
        #vin should 17 to 20 return on multiple lines
        self.conn.obd2_write(self.connection, 'ATL1')
        #headeres off
        self.conn.obd2_write(self.connection, 'ATH0')
        #removes spaces
        self.conn.obd2_write(self.connection, 'ATS0')
        #Allow Long (>7 byte) messages
        self.conn.obd2_write(self.connection, 'ATAL')
        #ask obd2 for vin
        self.conn.obd2_write(self.connection, '0902')
        read = self.conn.obd2_read_raw(self.connection)

        print read
        my_str = '\t'.join([line.strip() for line in read])
        print my_str.replace(" ", "")

        #ascii_read = converters.hex_to_ascii(read)
        #print ascii_read

    def get_data(self, property):
        self.open_close()

        self.propertiy_dict = {}

        for each in self.sensors.get(property):
            value = self.sensors.get(property).get(each)

            self.conn.obd2_write(self.connection, value)
            time.sleep(.15)
            read = self.conn.obd2_read(self.connection)
            self.dh.update_dict(self.propertiy_dict, value, read)

        return self.propertiy_dict

    def make_human(self):

        self.open_close()
        #Linefeeds On
        self.conn.obd2_write(self.connection, 'ATL1')
        #Headers On
        self.conn.obd2_write(self.connection, 'ATH1')
        #perform a Slow Initiation
        self.conn.obd2_write(self.connection, 'ATS1')
        #Allow Long (>7 byte) messages
        self.conn.obd2_write(self.connection, 'ATAL')
        #stream
        #self.conn.obd2_write(self.connection, 'ATMA')

    def obd2_innitialize(self):


        # this is still in prototype stage too.
        count = 0

        self.open_close()

        for each in self.sensors.get('startup_steps'):
            value = self.sensors.get('startup_steps').get(each)

            self.conn.obd2_write(self.connection, value)
            read = self.conn.obd2_read(self.connection)
            print 'read after {0}: {1}'.format(value, read)

        #Sensor("          Supported PIDs", "0100", hex_to_bitstring  ,""       ),
        self.conn.obd2_write(self.connection, '0100')
        read = self.conn.obd2_read(self.connection)
        print 'read after 0100: {0}'.format(read)
        #output: 41 00 BE 1F B8 10 where 41 00 is the header

        # Set the caller's desired protocol, then make a simple "0100" call to
        # make sure the ECU responds.  If we get anything back other than something
        # that starts with "41 00", it means the ELM can't talk to the OBD
        #system.

        #Sensor("     Coolant Temperature", "0105", temp              ,"C"      ),
        self.conn.obd2_write(self.connection, '0105')
        read = self.conn.obd2_read(self.connection)
        if read == 'STOPPED':
            print 'Car is not running, or not supported'

        print 'read after 0105: {0}'.format(read)
        # expected output: hex, 41 05 79
        # where 41 05 is the header and 79 is the hex value


    def get_acc_axes(self):

        axes = self.acc.getAxes(True)
        self.dh.update_dict(self.temp_dict, 'x_acc', axes['x'])
        self.dh.update_dict(self.temp_dict, 'y_acc', axes['y'])
        self.dh.update_dict(self.temp_dict, 'z_acc', axes['z'])

        print "   x = %.3fG" % ( axes['x'] )
        print "   y = %.3fG" % ( axes['y'] )
        print "   z = %.3fG" % ( axes['z'] )

    def main(self):

        self.ph.set_logger(self.logger_config)
        logger = logging.getLogger("obd2")
        logger.info('testing_122')


        mnt = self.ph.check_disk('/mnt')
        mnt_percent = mnt.percent
        message = 'mnt used: {0}%'.format(mnt_percent)
        lcd.set_lcd(message, 0, True)


        self.get_vin()

#        self.obd2_innitialize()

        now = time.time()
        message = 'epoc: {0}'.format(now)
        lcd.set_lcd(message, 8, False)

#        mode09 = self.get_data('mode09')
#        print mode09


        # this will be put into a loop based on the sample_rate found
        print self.sample_rate

        message = 'sample rate: {0}'.format(self.sample_rate)
        lcd.set_lcd(message, 16, False)

        # this will be used for debug
        print self.number_of_loops

        count = 0
        while (count < self.number_of_loops):
            now = time.time()
            self.temp_dict = {'now': str(now)}

            #time.sleep(self.sample_rate)
            count = count + 1

            sensors = self.get_data('sensors')
            message = 'count is: {0}'.format(count)
            lcd.set_lcd(message, 24, False)
            self.dh.update_dict(self.temp_dict, 'sensors_data', sensors)
            print self.temp_dict

        #self.get_acc_axes()

        #self.make_human()

        #TODO folder will be vin
        folder_location = os.path.join(self.application_properties.get('output').get('data_output_folder'), 'vin')
        self.ph.check_folder(folder_location)
        file_location = os.path.join(folder_location, '{0}.pkl'.format(now))
        #self.ph.write_csv(sorted_temp_dict, file_location)
        self.ph.write_pickle(self.temp_dict, file_location)


if __name__ == '__main__':
    Obd2Link().main()