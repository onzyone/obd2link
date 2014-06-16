import gaugette.ssd1306

# Sets our variables to be used later
RESET_PIN = 15
DC_PIN    = 16
TEXT = ''

def set_lcd(message, position, clear):

    #define positions
    # 0, 8, 16, 24
    message = str(message)
    led = gaugette.ssd1306.SSD1306(reset_pin=RESET_PIN, dc_pin=DC_PIN)
    if clear:
        print 'clearing? {0}'.format(clear)
        led.begin()
        led.clear_display()

    # The actual printing of TEXT
    led.draw_text2(0, position, message, 1)
    led.draw_text2(0, position, message, 1)
    led.draw_text2(0, position, message, 1)
    led.draw_text2(0, position, message, 1)
    led.display()
