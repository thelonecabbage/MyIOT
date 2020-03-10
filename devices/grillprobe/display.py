# https://micropython-oled.readthedocs.io/en/latest/content/getting_started.html#font-awesome
from machine import Pin, I2C
from oled.lazy import Write, GFX, SSD1306_I2C
from oled.fonts import ubuntu_mono_15 # , ubuntu_mono_20

width = 128
height = 32
sda = Pin(2)
scl = Pin(0)

i2c = I2C(scl=scl, sda=sda)
oled = SSD1306_I2C(width, height, i2c)
gfx = GFX(width, height, oled.pixel)

write15 = Write(oled, ubuntu_mono_15)

def clear():
    oled.fill(0) # clear screen

def row_display(lines = [], color=1):
    row_height = int(height / len(lines))
    for row, line in enumerate(lines, start=0):
        col_width = int(width / len(line))
        for col, msg in enumerate(line, start=0):
            if msg:
                write15.text(msg, col_width * col, row_height * row + 1, color, abs(color - 1))

def row_seperator(yPos = None):
    yPos = None or height // 2 
    gfx.line(0, yPos, width, yPos, 1)

# write15.text("Espresso IDE", 0, 0)
# oled.show()
# import display
# display.row_display([['SET', '444', '444', '888'], ['C', '444', '444', '888']])
# display.oled.show()
# display.row_seperator()
# display.row_display([['', '444', '', ''], ['', '444', '', '']], 0)
# display.oled.show()
