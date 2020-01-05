import hid
import time


class BridgeModuleException(Exception):
    pass


class BridgeModule:

    def __init__(self):

        try:
            self._hid = hid.Device(vid=0x0403, pid=0x6030)
        except hid.HIDException:
            raise BridgeModuleException

        if self._hid.manufacturer != 'FTDI' or self._hid.product != 'FT260':
            raise BridgeModuleException

        self._i2c_init()

        self._i2c_bus = None
        self.i2c_select(0)

    def led_set(self, state):

        if state:
            self._feature_out(b'\xb0\x00\x00\x80\x80')
        else:
            self._feature_out(b'\xb0\x00\x00\x00\x80')

    def led_pulse(self, duration=1):

        self.led_set(False)
        time.sleep(0.1)
        self.led_set(True)
        time.sleep(duration)
        self.led_set(False)

    def i2c_select(self, bus):

        if self._i2c_bus != bus:
            if not self.i2c_write(0x70, b'\x01' if bus == 0 else b'\x02'):
                raise BridgeModuleException
            self._i2c_bus = bus

    def i2c_write(self, address, data, generate_stop=True):

        time.sleep(0.1)

        flag = 0x06 if generate_stop else 0x02
        length = len(data)
        buffer = bytes([0xd0 + (length - 1) // 4, address, flag, length])

        self._i2c_wait()
        self._interrupt_out(buffer + data)
        bus_status = self._i2c_wait(accept_bus_busy=not generate_stop)

        return True if (bus_status & 0x1e) == 0 else False

    def i2c_read(self, address, length, repeated_start=False):

        if not repeated_start:
            time.sleep(0.1)

        flag = 0x07 if repeated_start else 0x06
        buffer = bytes([0xc2, address, flag, length, length >> 8])

        self._i2c_wait(accept_bus_busy=repeated_start)
        self._interrupt_out(buffer)
        data = self._interrupt_in(64)
        bus_status = self._i2c_wait()

        if data[1] != length:
            raise BridgeModuleException

        if bus_status != 0x20:
            return False

        return data[2:2 + length]

    def _i2c_init(self):

        self._i2c_reset()
        self._i2c_set_speed()

    def _i2c_reset(self):

        self._feature_out(b'\xa1\x20')

    def _i2c_set_speed(self):

        self._feature_out(b'\xa1\x22\x64\x00')
        status = self._i2c_get_status()
        if status[2:4] != b'\x64\x00':
            raise BridgeModuleException

    def _i2c_get_status(self):

        status = self._feature_in(0xc0, 5)
        if status[0:1] != b'\xc0':
            raise BridgeModuleException

        return status

    def _i2c_wait(self, accept_bus_busy=False):

        while True:
            bus_status = self._i2c_get_status()[1]
            if (bus_status & 0x01) == 0:
                if (bus_status & 0x20) != 0:
                    break
                if accept_bus_busy and (bus_status & 0x40) != 0:
                    break
            time.sleep(0.1)

        return bus_status

    def _feature_out(self, data):

        try:
            if self._hid.send_feature_report(data) != len(data):
                raise BridgeModuleException
        except hid.HIDException:
            raise BridgeModuleException

    def _feature_in(self, report_id, size):

        try:
            return self._hid.get_feature_report(report_id, size)
        except hid.HIDException:
            raise BridgeModuleException

    def _interrupt_out(self, data):

        try:
            if self._hid.write(data) != len(data):
                raise BridgeModuleException
        except hid.HIDException:
            raise BridgeModuleException

    def _interrupt_in(self, size):

        try:
            return self._hid.read(size, timeout=None)
        except hid.HIDException:
            raise BridgeModuleException
