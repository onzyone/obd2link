import obd2_connection
import obd2_constents


def get_connection():

    port = '/dev/ttyUSB0' # this will need to be taken care of by a get call later on
    baudrate = 115200

    conn = obd2_connection.Obd2Connection()
    connection = conn.obd2_connection(port=port, baudrate=baudrate)

    return connection

def get_constenst():
    at_constents = obd2_constents.AT_CODES

    print at_constents

def main():
    connection = get_connection()
    get_constenst()
    
if __name__ == '__main__':
    main()