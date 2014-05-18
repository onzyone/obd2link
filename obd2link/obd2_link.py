import obd2_connection
import obd2_constants


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

def get_version(connection):

    conn = obd2_connection.Obd2Connection()
    conn.obd2_write(connection, 'ATI')
    read = conn.obd2_read(connection)

    print read

def main():
    connection = get_connection()
    get_version(connection)
    get_constants()

if __name__ == '__main__':
    main()