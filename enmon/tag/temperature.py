import time


class TemperatureTagException(Exception):
    pass


class TemperatureTag:

    def __init__(self, bm, bus, address):

        self._bm = bm
        self._bus = bus
        self._address = address
        self._initialized = False

    def measure(self):

        try:

            self._bm.i2c_select(self._bus)

            if not self._initialized:
                self._write(0x01, 0x0180)
                time.sleep(0.1)
                self._initialized = True

            self._write(0x01, 0x8180)
            time.sleep(0.1)

            if (self._read(0x01) & 0x8100) != 0x8100:
                raise TemperatureTagException

            value = self._read(0x00).to_bytes(2, byteorder='big')
            value = int.from_bytes(value, byteorder='big', signed=True)
            value = round((value >> 4) / 16.0, 1)

            return value

        except TemperatureTagException:

            self._initialized = False
            raise

    def _write(self, address, value):

        if not self._bm.i2c_write(self._address, bytes([address]) + value.to_bytes(2, byteorder='big')):
            raise TemperatureTagException

    def _read(self, address):

        if not self._bm.i2c_write(self._address, bytes([address]), generate_stop=False):
            raise TemperatureTagException

        data = self._bm.i2c_read(self._address, 2, repeated_start=True)
        if not data:
            raise TemperatureTagException

        return int.from_bytes(data, byteorder='big')
