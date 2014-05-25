import obd2_connection
import obd2_constants
import time

import file_io


def get_connection():

    port = '/dev/ttyUSB0' # this will need to be taken care of by a get call later on
    baudrate = 115200

    conn = obd2_connection.Obd2Connection()
    connection = conn.obd2_connection(port=port, baudrate=baudrate)

    return connection

def get_constants():
    constants = obd2_constants.CONSTANTS
    for key, value in constants.items():
        print key, value

def get_sensors(connection):

    temp_dict = {}

    conn = obd2_connection.Obd2Connection()
    conn.obd2_close(connection)
    conn.obd2_open(connection)

    sensors = obd2_constants.SENSORS
    for key, value in sensors.items():
#        print k, v
        for key, value in value.items():
            if key == 'hex':
                conn.obd2_write(connection, value)
                read = conn.obd2_read(connection)
                temp_dict.update({key: read})
                print 'after reading bus: ' + read
            else:
                print key, value

    print temp_dict
    file_io.write_csv(temp_dict)

def get_version(connection):

    conn = obd2_connection.Obd2Connection()
    conn.obd2_close(connection)
    conn.obd2_open(connection)
    conn.obd2_is_open(connection)

    conn.obd2_write(connection, 'ATI')
    read = conn.obd2_read(connection)

    print 'read after ATI: ' + read

def odb2_innitialize(connection):

    count = 0
    conn = obd2_connection.Obd2Connection()
    conn.obd2_close(connection)
    conn.obd2_open(connection)

    conn.obd2_write(connection, 'ATZ')
    read = conn.obd2_read(connection)

    print 'read after ATZ: ' + read

    time.sleep(5)

    #echo off
    conn.obd2_write(connection, 'ATE0')
    read = conn.obd2_read(connection)

    print 'read after ATE0: ' + read

    conn.obd2_write(connection, 'ATDP')
    read = conn.obd2_read(connection)

    print 'read after ATDP: ' + read

    #not connected: UNABLE TO CONNECTSEARCHING


    #Sensor("          Supported PIDs", "0100", hex_to_bitstring  ,""       ),
    conn.obd2_write(connection, '0100')
    time.sleep(5)
    read = conn.obd2_read(connection)
    print 'read after 0100: ' + read

    #Sensor("     Coolant Temperature", "0105", temp              ,"C"      ),
    conn.obd2_write(connection, '0105')
    time.sleep(5)
    read = conn.obd2_read(connection)
    # expected output: hex, 41 05 79
    # where 41 05 is the header and 79 is the hex value
    print 'read after 0105: ' + read



def main():
    connection = get_connection()
    #get_version(connection)
    odb2_innitialize(connection)
    #get_constants()
    get_sensors(connection)

if __name__ == '__main__':
    main()