import time


class HumidityTagException(Exception):
    pass


class HumidityTag:

    def __init__(self, bm, bus, address):

        self._bm = bm
        self._bus = bus
        self._address = address
        self._initialized = False

    def measure(self):

        try:

            self._bm.i2c_select(self._bus)

            if not self._initialized:
                self._write(0xfe)
                time.sleep(0.1)
                self._initialized = True

            self._write(0xf5)
            time.sleep(0.1)
            humidity = round(-6 + 125 * self._read() / 65536, 1)

            self._write(0xf3)
            time.sleep(0.1)
            temperature = round(-46.85 + 175.72 * self._read() / 65536, 1)

            return (humidity, temperature)

        except HumidityTagException:

            self._initialized = False
            raise

    def _write(self, value):

        if not self._bm.i2c_write(self._address, bytes([value])):
            raise HumidityTagException

    def _read(self):

        data = self._bm.i2c_read(self._address, 2)
        if not data:
            raise HumidityTagException

        return int.from_bytes(data, byteorder='big')
