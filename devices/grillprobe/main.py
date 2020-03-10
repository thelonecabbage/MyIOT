import time
from machine import Pin, PWM
import display
from utils import avg, list_max
from thermocouples import get_telemetry
from server import device_update_server
from secrets import DEVICE_ID
from PID import PID
from PID import PIDParams

def main():
    settings = {}
    last_telemetry_time = 0
    last_grill = 0
    last_probe = [0, 0]
    max_telemetry_time_ms = 60 * 1000
    max_telemetry = 10
    grill_target = 150
    settings = {
        "grillTarget": 177,
        "probeTargets": [0, 0],
        "probeIcons": [],
        "probeNames": ['', '']
    }
    grill_list = []
    probe_list = [[], []]
    last_telemetry_time = time.ticks_ms() 

    kP= 5 # 1.5
    kI= 1 # .02
    kD= 5 # 10
    fanMin = 0
    fanMax = 1023

    pidParams = PIDParams(input=0, output=0, setpoint=grill_target)
    pid = PID(params=pidParams, kP=kP, kI=kI, kD=kD)
    pid.setOutputLimits(200, 1023)
    pid.setMode(PID.AUTOMATIC)

    p16 = Pin(16)
    pwm = PWM(p16)
    pwm.freq(500)
    pwm.duty(0)

    cnt = 0
    while True:
        cnt += 1
        t_start = time.ticks_ms()
        probe = [0, 0]
        grill, probe[0], probe[1] = get_telemetry()

        if grill is not None:
            grill_list.append(grill)
            grill_list = list_max(grill_list, max_telemetry)
            print('len(grill_list)=', len(grill_list))
        for i in range(0, 2):
            if probe[i] is not None:
                probe_list[i].append(probe[i])
                probe_list[i] = list_max(probe_list[i], max_telemetry)
                print('len(probe_list[' + str(i) + '])=', len(probe_list[i]))


        grill = avg(grill_list, 0) or 0
        for i in range(0, 2):
            probe[i] = avg(probe_list[i], 0) or 0

        telemetry = {}
        if not int(grill) == int(last_grill):
            telemetry['grill'] = grill
        for i in range(0, 2):
            if not int(probe[i]) == int(last_probe[i]):
                telemetry['probes'] = telemetry.get('probes', last_probe.copy()) 
                telemetry['probes'][i] = probe[i]

        t_delta = time.ticks_ms() - last_telemetry_time
        if len(telemetry) or t_delta >= max_telemetry_time_ms:
            print({'telemetry': telemetry})
            telemetry['pwm'] = pidParams.output
            response = device_update_server(id=DEVICE_ID, telemetry=telemetry)
            print(response)
            if response:
                last_grill = grill
                for i in range(0, 2):
                    last_probe[i] = probe[i]
                settings = response['result']['settings']
                grill_target = settings['grillTarget']
                last_telemetry_time = time.ticks_ms()

        
    # PID
        pidParams.setpoint = grill_target
        pidParams.input = grill
        res = pid.compute()
        pwm.duty(int(pidParams.output))
        print('PWM set', res, pidParams.setpoint, pidParams.input, pidParams.output)
    # Update display
        probe_target = settings['probeTargets']
        probe_names = settings['probeNames']
       
        if cnt % 2 == 1:
            probe_msgs = [str(int(probe_target[0])), str(int(probe_target[1]))]
        else:
            probe_msgs = [probe_names[0][:4], probe_names[1][:4]]
        
        display.clear()
        lines = [
            ['C', str(int(grill)), str(int(probe[0])), str(int(probe[1]))],
            ['Set', str(int(grill_target)), probe_msgs[0], probe_msgs[1]]
        ]
        alt_lines = [
            ['', str(int(grill)), '', ''],
            ['', str(int(grill_target)), '', '']
        ]
        display.row_display(lines)
        display.row_display(alt_lines, 0)
        display.row_seperator()
        display.oled.show()

        # compensate time, to keep 1s intervals
        t_delta = time.ticks_ms() - t_start
        time.sleep_ms(1000 - t_delta)

main()
