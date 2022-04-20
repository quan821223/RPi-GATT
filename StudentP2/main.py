'''
environment : linux
debug environment : linux & windows
package : gatt, blueman
HW : serial device *2, cable *1, raspberry Pi 3/4 *1

pre-condition :
1. Write the UUIDs of DUT to ProjectUUID.py
2. need to connect DUT by system.

the format of communication :
------ASCII------
- b0 p [project]
- b0 c [macaddress]
- b0 w [characteristic][data]
'''
try:
    import dbus
    import dbus.mainloop.glib
except ImportError:
    import sys
    print("Module 'dbus' not found")
    print("Please run: sudo apt-get install python3-dbus")
    print("See also: https://github.com/getsenic/gatt-python#installing-gatt-sdk-for-python")
    sys.exit(1)

import re
from gi.repository import GObject



from setseril import Serialcom
from ObserverOper import Serilcenter, ChangeProject, SendtoChara, Connecttodevice
import time
import gatt
import threading
import datetime

class AnyDeviceManager(gatt.DeviceManager):

    def device_discovered(self, device):
        print("Discovered [%s] %s" % (device.mac_address, device.alias()))

    def loop_start(self):
        self._thread = threading.Thread(target=self.run, daemon = True)
#         self._thread.daemon = True
        self._thread.setDaemon(True)
        self._thread.start()

    def loop_stop(self):
        self.stop()
        

class AnyDevice(gatt.Device):
    def __init__(self, mac_address, manager, uartport):

        self.characteristic2 = None
        self.characteristic3 = None

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
            if s.uuid == projectuuids.service.lower())

        self.characteristic2 = next(
            c for c in service.characteristics
            if c.uuid == projectuuids.chara2.lower())

        self.characteristic3 = next(
            c for c in service.characteristics
            if c.uuid == projectuuids.chara3.lower())

        characteristic1 = next(
            c for c in service.characteristics
            if c.uuid == projectuuids.chara1.lower())
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
        hexstr = ''.join(['%02x' % b + ' 'for b in value])     
        display_msg_table(hexstr, 'r')        
        myUart.write(value)
        time.sleep(0.1)

def display_msg_table(msg, type_msg = ''):
    
    nowTime = datetime.datetime.now()
    if type_msg =='r' or type_msg =='R':    
        print('[%s][R] %s' %(nowTime, str(msg)))
    elif type_msg =='s'or type_msg =='S':
        print('[%s][S] %s' %(nowTime, str(msg)))
    elif type_msg =='':
        print('[%s] %s' %(nowTime, str(msg)))
    else:
        print('[%s][%s] %s' %( nowTime, type_msg, str(msg)))
        
        
if __name__ == '__main__':

    comter = Serilcenter()

    getRegister = ChangeProject()
    sendRegister = SendtoChara()
    ConnectRegister = Connecttodevice()

    comter.addObserver(getRegister)
    comter.addObserver(sendRegister)
    comter.addObserver(ConnectRegister)

    Seriset = Serialcom()
    Seriset.port_Info()
    Seriset.port_com()
    myUart = Seriset.Uart
    projectuuids =None
    comter.uartinterface = myUart
    '''
    testing mode
    '''
    IsDEBUGTEST = False
    comter.debugmode = IsDEBUGTEST

    if(not IsDEBUGTEST):
        manager = AnyDeviceManager(adapter_name='hci0')
#         manager.loop_start()

    while (True):

        count = myUart.inWaiting()
        comter.asignuartcom(myUart)
        if count is not 0:
            recdatas = myUart.readline()


            #check the head of CMD from PC controlled.
            if(recdatas[0] == 98 and recdatas[1] == 48):
                comter.setgetdata(recdatas)

                if(comter.IsChangeUUID):
                    projectuuids = comter.getprojectuuids
#                     nowTime = datetime.datetime.now()
#                     print('[' +  str(nowTime) + '] \n')
#                     print('專案目前取用的uuids')
#                     print(projectuuids.service)
#                     print(projectuuids.chara1)
#                     print(projectuuids.chara2)
#                     print(projectuuids.chara3)
                    comter.IsChangeUUID=False

                if (comter.IsConnectRequir):
                    if (not IsDEBUGTEST):
                        print('connected')
                        manager = AnyDeviceManager(adapter_name='hci0')
                        bleDevices = AnyDevice(mac_address = comter.MACaddress, manager = manager, uartport = myUart)
                        bleDevices.connect()
                        time.sleep(1)
                        ''' Don't remove this CMD'''
                        manager.loop_start()
#                         manager.run()
                        comter.IsConnectRequir = False

                if(comter.IsSendData):
                    if(comter.Ischara2):
                            for eachData in comter.databuffer:
                                if(not IsDEBUGTEST):
                                    bleDevices.characteristic2.write_value(eachData)
                                time.sleep(.17)
                                nowTime = datetime.datetime.now()
                                display_msg_table(''.join(['%02x' % b + ' 'for b in eachData])  , 'f2')   
                                #print('['+ str(nowTime) + '] ' + str(eachData))



                    if (comter.Ischara3):
                            for eachData in comter.databuffer:
                                if (not IsDEBUGTEST):
                                    bleDevices.characteristic3.write_value(eachData)
                                time.sleep(.17)
                                nowTime = datetime.datetime.now()
                                display_msg_table(''.join(['%02x' % b + ' 'for b in eachData]), 'f3')   
                                #print('['+ str(nowTime) + '] ' + str(eachData))

                    comter.databuffer = []
                    comter.Ischara2 = False
                    comter.Ischara3 = False
                    comter.IsSendData =False
                    comter.IsChangeUUID=False
                myUart.flushOutput()
                myUart.flushInput()
                time.sleep(.01)

manager.loop_stop()
