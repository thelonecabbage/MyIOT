import time
from max6675 import MAX6675
from machine import Pin

so = Pin(23, Pin.IN)
sck = Pin(21, Pin.OUT)
cs_list = [
    Pin(22, Pin.OUT),
    Pin(18, Pin.OUT),
    Pin(5, Pin.OUT)
]

mx6675 =  []

for cs in cs_list:
    mx = MAX6675(sck, cs , so)
    mx6675.append(mx)
    mx.refresh()

telemetry_ticks_ms = 0
def get_telemetry():
    t_start = time.ticks_ms()
    telemetry = []
    for mx in mx6675:
        error = mx.error()
        temp = mx.read()
        telemetry.append(temp if not error else None)
        if error:
            mx.refresh()
    telemetry_ticks_ms = time.ticks_ms() - t_start
    return telemetry
