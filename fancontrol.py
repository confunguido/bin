#!/usr/bin/env python3

import subprocess
import time

from gpiozero import OutputDevice
from gpiozero import CPUTemperature

ON_THRESHOLD = 45  # (degrees Celsius) Fan kicks on at this temperature.
OFF_THRESHOLD = 35  # (degress Celsius) Fan shuts off at this temperature.
SLEEP_INTERVAL = 5  # (seconds) How often we check the core temperature.
GPIO_PIN = 17  # Which GPIO pin you're using to control the fan.


def get_temp():
    cpu = CPUTemperature()
    return cpu.temperature

if __name__ == '__main__':
    # Validate the on and off thresholds
    if OFF_THRESHOLD >= ON_THRESHOLD:
        raise RuntimeError('OFF_THRESHOLD must be less than ON_THRESHOLD')

    fan = OutputDevice(GPIO_PIN)

    while True:
        temp = get_temp()
        print("Temp is %.2f" % temp)
        # Start the fan if the temperature has reached the limit and the fan
        # isn't already running.
        # NOTE: `fan.value` returns 1 for "on" and 0 for "off"
        if temp > ON_THRESHOLD and not fan.value:
            # fan.on()
            print("Turning fan on")

        # Stop the fan if the fan is running and the temperature has dropped
        # to 10 degrees below the limit.
        elif fan.value and temp < OFF_THRESHOLD:
            # fan.off()
            print("Turning fan Off")

        time.sleep(SLEEP_INTERVAL)
