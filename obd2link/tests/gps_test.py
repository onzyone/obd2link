#! /usr/bin/python
# Written by Dan Mandle http://dan.mandle.me September 2012
# License: GPL 2.0

import os
from gps import *
import time
import threading

#seting the global variable
gpsd = None

#clear the terminal (optional)
os.system('clear')

class GpsPoller(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        #bring it in scope
        global gpsd
        #starting the stream of info
        gpsd = gps(mode=WATCH_ENABLE)
        self.current_value = None
        #setting the thread running to true
        self.running = True

    def run(self):
        global gpsd
        while gpsp.running:
        #this will continue to loop and grab EACH set of gpsd info to clear the buffer
            gpsd.next()

if __name__ == '__main__':
    # create the thread
    gpsp = GpsPoller()
    try:
        # start it up
        gpsp.start()
        while True:
            #It may take a second or two to get good data
            #print gpsd.fix.latitude,', ',gpsd.fix.longitude,'  Time: ',gpsd.utc

            os.system('clear')

            print
            print ' GPS reading'
            print '----------------------------------------'
            print 'latitude    ' , gpsd.fix.latitude
            print 'longitude   ' , gpsd.fix.longitude
            print 'time utc    ' , gpsd.utc,' + ', gpsd.fix.time
            print 'altitude (m)' , gpsd.fix.altitude
            print 'eps         ' , gpsd.fix.eps
            print 'epx         ' , gpsd.fix.epx
            print 'epv         ' , gpsd.fix.epv
            print 'ept         ' , gpsd.fix.ept
            print 'speed (m/s) ' , gpsd.fix.speed
            print 'climb       ' , gpsd.fix.climb
            print 'track       ' , gpsd.fix.track
            print 'mode        ' , gpsd.fix.mode
            print
            print 'sats        ' , gpsd.satellites

            #set to whatever
            time.sleep(5)

    #when you press ctrl+c
    except (KeyboardInterrupt, SystemExit):
        print "\nKilling Thread..."
        gpsp.running = False
        # wait for the thread to finish what it's doing
        gpsp.join()
    print "Done.\nExiting."