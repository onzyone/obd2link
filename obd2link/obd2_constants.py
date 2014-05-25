
CONSTANTS = { 'AT_CODES' : {'I' : 'version ID',
                            'DP' : 'display protocol',
                            'SP' : {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}},
              'ST_CODES' : {'DI' : 'device hardware ID',
                            'I' : 'firmware ID',
                            'MFR' : 'device manufacturer ID',
                            'SN' : 'device serial number'}}

SENSORS = { 0: {'hex': '010C', 'description': 'Engine RPM (RPM)', 'measurement': 'rpm'},
            1: {'hex': '0106', 'description': 'Short Term Fuel Trim', 'measurement': 'rpm'},
            2: {'hex': '0107', 'description': 'Long Term Fuel Trim', 'measurement': 'rpm'},
            3: {'hex': '0110', 'description': 'Mass air flow rate (g/s) -(Air Flow Rate lb/min)', 'measurement': 'lb/min'},
            }

#ATSP

#Usage: ATSPn, where n is 0 to 9.
#Set desired communication protocol.

#0	Automatic protocol detection
#1	SAE J1850 PWM (41.6 kbaud)
#2	SAE J1850 VPW (10.4 kbaud)
#3	ISO 9141-2 (5 baud init, 10.4 kbaud)
#4	ISO 14230-4 KWP (5 baud init, 10.4 kbaud)
#5	ISO 14230-4 KWP (fast init, 10.4 kbaud)
#6	ISO 15765-4 CAN (11 bit ID, 500 kbaud)
#7	ISO 15765-4 CAN (29 bit ID, 500 kbaud)
#8	ISO 15765-4 CAN (11 bit ID, 250 kbaud) - used mainly on utility vehicles and Volvo
#9	ISO 15765-4 CAN (29 bit ID, 250 kbaud) - used mainly on utility vehicles and Volvo
