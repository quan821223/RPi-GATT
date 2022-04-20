import gatt
import threading
import time




class AnyDeviceManager(gatt.DeviceManager):

    def device_discovered(self, device):
        print("Discovered [%s] %s" % (device.mac_address, device.alias()))

    def loop_start(self):
        self._thread = threading.Thread(target=self.run)
        self._thread.daemon = True
        self._thread.start()

    def loop_stop(self):
        self.stop()


class AnyDevice(gatt.Device):
    def __init__(self, mac_address, manager, ble_uuids, uartport):

        self.characteristic2 = None
        self.characteristic3 = None
        self.serive_uuid = ble_uuids.service
        self.chara1 = ble_uuids.chara1
        self.chara2 = ble_uuids.chara2
        self.chara3 = ble_uuids.chara3
        self.myUart = uartport
        super().__init__(mac_address, manager, managed=True)

    def connect_succeeded(self):
        super().connect_succeeded()
        print("[%s] Connected" % (self.mac_address))

    def connect_failed(self, error):
        super().connect_failed(error)
        print("[%s] Connection failed: %s" % (self.mac_address, str(error)))

    def disconnect_succeeded(self):
        super().disconnect_succeeded()
        print("[%s] Disconnected" % (self.mac_address))

    def services_resolved(self):
        super().services_resolved()
        service = next(
            s for s in self.services
            if s.uuid == self.serive_uuid.lower())

        self.characteristic2 = next(
            c for c in service.characteristics
            if c.uuid == self.chara2.lower())

        self.characteristic3 = next(
            c for c in service.characteristics
            if c.uuid == self.chara3.lower())

        characteristic1 = next(
            c for c in service.characteristics
            if c.uuid == self.chara1.lower())
        #         FFF3.enable_notifications()
        characteristic1.enable_notifications()

    def characteristic_enable_notifications_succeeded(self, characteristic):
        super().characteristic_enable_notifications_succeeded(characteristic)
        print("[%s] notify ok" % (self.mac_address))

    def characteristic_enable_notifications_failed(self, characteristic, error):
        super().characteristic_enable_notifications_failed(characteristic, error)
        print("[%s] notify err. %s" % (self.mac_address, error))

    def characteristic_write_value_succeeded(self, characteristic):
        super().characteristic_write_value_succeeded(characteristic)
        print("[%s] wr ok" % (self.mac_address))

    def characteristic_write_value_failed(self, characteristic, error):
        super().characteristic_write_value_failed(characteristic, error)
        print("[%s] wr err %s" % (self.mac_address, error))

    def characteristic_value_updated(self, characteristic, value):
        print(value)
        self.myUart.write(value)
        # Seriset.Uart.write(value)
        time.sleep(0.1)