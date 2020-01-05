import click
import hid
import time

from .bridge_module import BridgeModule, BridgeModuleException
from .climate_module import ClimateModule, ClimateModuleException


def main():

    try:

        bridge_module = BridgeModule()
        bridge_module.led_pulse(0.1)

        climate_module = ClimateModule(bridge_module)

        while True:

            data = climate_module.measure()

            print("Temperature 1", data['temperature1'], "°C")
            print("Temperature 2", data['temperature2'], "°C")
            print("Humidity", data['humidity'], "%")
            print("Pressure", data['pressure'], "hPa")
            print("Altitude", data['altitude'], "m")
            print("Illuminance", data['illuminance'], "lux")

    except BridgeModuleException:
        raise

    except KeyboardInterrupt:
        pass


main()
