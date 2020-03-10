# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import webrepl
import network
from secrets import WIFI_SSID, WIFI_PASSWORD
wlan = network.WLAN(network.STA_IF) # create station interface
wlan.active(True)       # activate the interface
wlan.connect(WIFI_SSID, WIFI_PASSWORD)

webrepl.start()
