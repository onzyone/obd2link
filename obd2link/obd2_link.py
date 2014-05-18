import obd2_connection


def get_connection():

    port='/dev/ttyUSB0' # this will need to be taken care of by a get call later on
    baudrate=115200

    conn = obd2_connection.Obd2Connection()
    connection = conn.obd2_connection( port=port, baudrate=baudrate)

    print connection