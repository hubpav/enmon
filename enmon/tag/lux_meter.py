import time


class LuxMeterTagException(Exception):
    pass


class LuxMeterTag:

    def __init__(self, bm, bus, address):

        self._bm = bm
        self._bus = bus
        self._address = address
        self._initialized = False

    def measure(self):

        try:

            self._bm.i2c_select(self._bus)

            if not self._initialized:
                self._write(0x01, 0xc810)
                time.sleep(1)
                self._initialized = True

            self._write(0x01, 0xca10)
            time.sleep(2)

            if (self._read(0x01) & 0x0680) != 0x0080:
                raise LuxMeterTagException

            value = self._read(0x00)
            value = (value & 0xffff) * (1 << (value >> 12))
            value = round(value * 0.01)

            return value

        except LuxMeterTagException:

            self._initialized = False
            raise


    def _write(self, address, value):

        if not self._bm.i2c_write(self._address, bytes([address]) + value.to_bytes(2, byteorder='big')):
            raise LuxMeterTagException

    def _read(self, address):

        if not self._bm.i2c_write(self._address, bytes([address]), generate_stop=False):
            raise LuxMeterTagException

        data = self._bm.i2c_read(self._address, 2, repeated_start=True)
        if not data:
            raise LuxMeterTagException

        return int.from_bytes(data, byteorder='big')
