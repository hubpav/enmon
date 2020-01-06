from .__info__ import VERSION

import click
import hid
import time

from .bridge_module import BridgeModule, BridgeModuleException
from .climate_module import ClimateModule, ClimateModuleException


@click.group()
@click.version_option(version=VERSION)
def cli():
    pass


@cli.command()
@click.option('--loop', is_flag=True, default=False, help='Enable measurement in the infinite loop.')
def measure(loop):
    '''Perform sensor measurement.'''

    try:

        bridge_module = BridgeModule()
        bridge_module.led_pulse(0.1)

        climate_module = ClimateModule(bridge_module)

        while True:

            data = climate_module.measure()

            print("Temperature", data['temperature'], "°C")
            print("Humidity", data['humidity'], "%")
            print("Pressure", data['pressure'], "hPa")
            print("Altitude", data['altitude'], "m")
            print("Illuminance", data['illuminance'], "lux")

            if not loop:
                break

    except BridgeModuleException:
        raise


@cli.command()
def pulse():
    '''Pulse the on-board LED and exit.'''

    try:

        bridge_module = BridgeModule()
        bridge_module.led_pulse(0.3)
        time.sleep(0.3)
        bridge_module.led_pulse(0.3)
        time.sleep(0.3)
        bridge_module.led_pulse(0.3)

    except BridgeModuleException:
        raise


def main():

    try:
        cli()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
