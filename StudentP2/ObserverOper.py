from ObserverClass import Register, UnRegister
from BLEmodule import AnyDeviceManager, AnyDevice
from ProjectUUID import projectUUID
import datetime
import math
import time
class Serilcenter(UnRegister):
    """數據中心"""
    def __init__(self):
        super().__init__()
        self.__getdata = ''
        self.__CMDtype = ''
        self.__getFuncTypeByte = b''
        self.__getsendCMD = ''
        self.__getfeature = ''
        self.__getstrdata = ''
        self.uartinterface = None
        self.MACaddress = default = '00:11:22:33:44:55'

        self.getprojectuuids = projectUUID()
        self.IsChangeUUID = False
        self.IsSendData = False
        self.IsConnectRequir = False
        self.IsOnelength = False
        self.IsTwolength = False
        self.Ischara1 = False
        self.Ischara2 = False
        self.Ischara3 = False
        self.databuffer = []

        self.debugmode = False


    def getBytedata(self):
        return self.__getdata

    def getCMDTypeStrData(self):
        self.__CMDtype = self.__getdata.strip(b'\r\n').decode('ascii').strip().split(' ')[1];
        return  self.__CMDtype

    def getfeaturechannel(self):
        if(self.__CMDtype.lower() == 'w'):
            self.__getfeature = self.__getdata.strip(b'\r\n').decode('ascii').strip().split(' ')[2]
        return   self.__getfeature.lower()

    def getSendCMD(self):
        if(self.__CMDtype.lower() == 'w'):
            self.__getsendCMD = self.__getdata.strip(b'\r\n').decode('ascii').strip().split(' ',3)[3]
        return   self.__getsendCMD

    def setgetdata(self, datafromcom):
        self.__getdata = datafromcom
        strdata = self.__getdata.strip(b'\r\n').decode('ascii')
        print( "get byte datas：" + strdata )
        self.notifyObservers()

    def projectUUIDs(self):
        return  self.getprojectuuids

    def BLEdeviceinfo(self):
        return self.bleDevices

    def getStrData(self):
        self.__getstrdata = self.__getdata.strip(b'\r\n').decode('ascii').split(' ');
        return self.__getstrdata

    def asignuartcom(self, uartdevice):
        self.uartinterface = uartdevice

    def uartcom(self):
        return self.uartinterface

    def split_list(l, n):
        for idx in range(0, len(l), n):
            yield l[idx:idx + n]

    def modityUartCMD(self,  uartdevice, msg):

        nowTime = datetime.datetime.now()
        print('[' +  str(nowTime) + '] ' + msg)

        strsplit = msg.split(' ')
        n = math.ceil(len(strsplit) / 11)

        if (n == 1):

            cmd_value = bytearray.fromhex(msg)
            self.uartinterface.write(bytes.fromhex('\r\n'.join(['%02X ' % b for b in cmd_value])))
            self.databuffer.append(cmd_value)


        elif n > 1:
            result = list(Serilcenter.split_list(msg, 3 * 11))
      
            for var in result:
                cmd_value = bytearray.fromhex(var)
                self.databuffer.append(cmd_value)
                self.uartinterface.write(cmd_value)
#                 self.databuffer.append(cmd_value)
#                 self.uartinterface.write(bytes.fromhex('\r\n'.join(['%02X ' % b for b in cmd_value])))
                time.sleep(.17)

class ChangeProject(Register):
    """
    該模式用於轉換專案
    """
    def update(self, Register, object):

        """ head/ type/ project. """
        Register.IsChangeUUID = True
        arrPCcmd = Register.getStrData()

        if isinstance(Register, Serilcenter)  and Register.getCMDTypeStrData().lower() == "p":
            if(arrPCcmd[2] == 'cxr6'):
                Register.projectUUIDs().cxr6()
                print("更改專案為cxr6")
                print( Register.projectUUIDs().service)
                print( Register.projectUUIDs().chara1)
                print( Register.projectUUIDs().chara2)
                print( Register.projectUUIDs().chara3)

            elif(arrPCcmd[2] == 'lite'):
                Register.projectUUIDs().cxrlift()
                print("更改專案為lite")
                print( Register.projectUUIDs().service)
                print( Register.projectUUIDs().chara1)
                print( Register.projectUUIDs().chara2)
                print( Register.projectUUIDs().chara3)

class SendtoChara(Register):
    """
    傳該模式用於傳輸
    """
    def update(self, Register, object):

        """ head/ type/ characteristic/data. """
        if isinstance(Register, Serilcenter) and Register.getCMDTypeStrData().lower() == "w":
            Register.IsSendData = True
            print("傳送數據")

            #send data to characteristic 2
            # if (Register.getfeaturechannel() == 'f2') and hasattr(   Register.bleDevices.characteristic2, "write_value"):
            if (Register.getfeaturechannel() == 'f2') :

                try:
                    Register.Ischara2 = True
                    Register.modityUartCMD(Register.uartcom(), Register.getSendCMD())

                except SystemExit:
                    print('send error !')
            # send data to characteristic 3
            # if (Register.getfeaturechannel() == 'f3') and hasattr(   Register.bleDevices.characteristic2, "write_value"):
            if (Register.getfeaturechannel() == 'f3') :
                try:
                    Register.Ischara3 = True
                    Register.modityUartCMD( Register.uartcom(), Register.getSendCMD())

                except SystemExit:
                    print('send error !')


# class ReadfromChara(Register):
#     """
#     傳該模式用於傳輸
#     """
#     def update(self, Register, object):
#
#         if isinstance(Register, Serilcenter) and Register.getCMDTypeStrData().lower() == "r":
#             print("讀取數據")

class Connecttodevice(Register):
    """
    傳該模式用於傳輸
    """
    def update(self, Register, object):
        """ head/ type/ characteristic/data. """
        if isinstance(Register, Serilcenter) and Register.getCMDTypeStrData().lower() == "c":

            
            arrPCcmd = Register.getStrData()
            if(len(arrPCcmd) >= 3):
                Register.IsConnectRequir = True
                print("與待測物連線")
                nowTime = datetime.datetime.now()  # 取得現在時間
                print('[' +  str(nowTime) + '] ' +  arrPCcmd[2].strip() )
                Register.MACaddress = arrPCcmd[2].strip()



''' 
    c:99   
    w:119
    r:114
    p:112  
'''