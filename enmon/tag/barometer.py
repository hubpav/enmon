import time


class BarometerTagException(Exception):
    pass


class BarometerTag:

    def __init__(self, bm, bus, address):

        self._bm = bm
        self._bus = bus
        self._address = address
        self._initialized = False

    def measure(self):

        try:

            self._bm.i2c_select(self._bus)

            if not self._initialized:
                self._reset()
                time.sleep(2)
                self._initialized = True

            self._write(0x26, 0xb8)
            self._write(0x13, 0x07)
            self._write(0x26, 0xba)

            time.sleep(2)

            if self._read(0x00) != 0x0e:
                raise BarometerTagException

            altitude = self._read(0x01, length=5)
            altitude = int.from_bytes(altitude[0:3], byteorder='big', signed=True)
            altitude = round((altitude >> 4) / 16, 1)

            self._write(0x26, 0x38)
            self._write(0x13, 0x07)
            self._write(0x26, 0x3a)

            time.sleep(2)

            if self._read(0x00) != 0x0e:
                raise BarometerTagException

            pressure = self._read(0x01, length=5)
            pressure = int.from_bytes(pressure[0:3], byteorder='big')
            pressure = round((pressure >> 4) / 400)

            return (pressure, altitude)

        except BarometerTagException:

            self._initialized = False
            raise

    def _reset(self):

        self._bm.i2c_write(self._address, bytes([0x26, 0x04]))

    def _write(self, address, value):

        if not self._bm.i2c_write(self._address, bytes([address, value])):
            raise BarometerTagException

    def _read(self, address, length=1):

        if not self._bm.i2c_write(self._address, bytes([address]), generate_stop=False):
            raise BarometerTagException

        data = self._bm.i2c_read(self._address, length, repeated_start=True)
        if not data:
            raise BarometerTagException

        return data if length > 1 else data[0]
