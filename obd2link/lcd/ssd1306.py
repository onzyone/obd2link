# OLEDip.py

# Meant for use with the Raspberry Pi and an Adafruit monochrome OLED display!

# This program interfaces with the OLED display in order to print your current IP address to it. The program trys
# several methods in order to accquire an IP address. For example if you are using a WiFi dongle your IP will be 
# different to when you are using a Ethernet cable. This program tests for both and if it can not detect one prints:
# 'NO INTERNET!' to the display. This code is perfect to run on boot when you want to find your Pi's IP address for
# SSH or VNC.

# This was coded by The Raspberry Pi Guy!

# Imports all of the necessary modules
import gaugette.ssd1306

# Sets our variables to be used later
RESET_PIN = 15
DC_PIN    = 16
TEXT = ''

def set_lcd(message, position, clear):

    led = gaugette.ssd1306.SSD1306(reset_pin=RESET_PIN, dc_pin=DC_PIN)
    if clear:
        led.begin()
        led.clear_display()


    #define positions
    # 0, 8, 16, 24
    message = str(message)


    # The actual printing of TEXT
    led.clear_display()
    led.draw_text2(0, position, message, 1)
    led.draw_text2(0, position, message, 1)
    led.draw_text2(0, position, message, 1)
    led.draw_text2(0, position, message, 1)
    led.display()
