import obd2_connection
import obd2_constants
import time


def get_connection():

    port = '/dev/ttyUSB0' # this will need to be taken care of by a get call later on
    baudrate = 115200

    conn = obd2_connection.Obd2Connection()
    connection = conn.obd2_connection(port=port, baudrate=baudrate)

    return connection

def get_constants():
    at_constants = obd2_constants.CONSTANTS
    for each in at_constants:
        print each

#def get_

def get_version(connection):

    conn = obd2_connection.Obd2Connection()
    conn.obd2_close(connection)
    conn.obd2_open(connection)

    if conn.obd2_is_open(connection):

        conn.obd2_write(connection, 'ATI')
        read = conn.obd2_read(connection)

        print read

def odb2_innitialize(connection):

    count = 0
    conn = obd2_connection.Obd2Connection()
    conn.obd2_close(connection)
    conn.obd2_open(connection)

    if conn.obd2_is_open(connection):

        conn.obd2_write(connection, 'atz')

        #echo off
        conn.obd2_write(connection, 'ate0')
        conn.obd2_write(connection, '0100')
        ready = conn.obd2_read(connection)

        print "what is ready looking like today?" + ready

        if ready == "BUSINIT: ...OK":
            ready = conn.obd2_read(connection)
            print "0100 response2: " + ready
            return None
        else:
            #ready=ready[-5:] #Expecting error message: BUSINIT:.ERROR (parse last 5 chars)
            time.sleep(5)
            if count == 5:
                ready = conn.obd2_read(connection)
                print "0100 response2: " + ready + " closing time"
                conn.obd2_close(connection)
                return None
            else:
                count = count + 1


def main():
    connection = get_connection()
    get_version(connection)
    odb2_innitialize(connection)
    get_constants()

if __name__ == '__main__':
    main()