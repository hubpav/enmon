from .tag.temperature import TemperatureTag, TemperatureTagException
from .tag.humidity import HumidityTag, HumidityTagException
from .tag.barometer import BarometerTag, BarometerTagException
from .tag.lux_meter import LuxMeterTag, LuxMeterTagException


class ClimateModuleException(Exception):
    pass


class ClimateModule:

    def __init__(self, bm):

        self._bm = bm

        self._temperature_tag = TemperatureTag(bm, bus=0, address=0x48)
        self._humidity_tag = HumidityTag(bm, bus=0, address=0x40)
        self._barometer_tag = BarometerTag(bm, bus=0, address=0x60)
        self._lux_meter_tag = LuxMeterTag(bm, bus=0, address=0x44)

    def measure(self):

        try:
            temperature1 = self._temperature_tag.measure()
        except TemperatureTagException:
            raise ClimateModuleException

        try:
            humidity, temperature2 = self._humidity_tag.measure()
        except HumidityTagException:
            raise ClimateModuleException

        try:
            pressure, altitude = self._barometer_tag.measure()
        except BarometerTagException:
            raise ClimateModuleException

        try:
            illuminance = self._lux_meter_tag.measure()
        except LuxMeterTagException:
            raise ClimateModuleException

        return {
            'temperature1': temperature1,
            'temperature2': temperature2,
            'humidity': humidity,
            'pressure': pressure,
            'altitude': altitude,
            'illuminance': illuminance
        }
