import serial
import serial.tools.list_ports
from ObserverOper import Serilcenter

class Serialcom(object):
    """
    The file is to initial Serial comport parameters
    """
    def __init__(self):
        self.Uart = serial.Serial(  # set parameters, in fact use your own :-)

            port='/dev/ttyUSB0',
            # port='COM11',
            baudrate=115200,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            rtscts=True
        )
        self.message = b''

    def port_Info(self):
        "be used serial comport informations."
        print(f'be used serial comport informations.')
        print(f'port : {self.Uart.port}')
        print(f'port : {self.Uart.port}')
        print(f'baudrate : {self.Uart.baudrate}')
        print(f'parity : {self.Uart.parity}')
        print(f'rtscts : {self.Uart.rts}')
        print(f'bytesize : {self.Uart.bytesize}')
        print(f'stopbits : {self.Uart.stopbits}')
        print(f'writeTimeout : {self.Uart.writeTimeout}')
        print(f'timeout : {self.Uart.timeout}')
        print(f'xonxoff : {self.Uart.xonxoff}')
        print(f'rtscts : {self.Uart.rtscts}')
        print(f'dsrdtr : {self.Uart.dsrdtr}')
        print(f'interCharTimeout : {self.Uart.interCharTimeout}')
        print(f'is_open : {self.Uart.is_open}\n')



    @staticmethod
    def port_com():

            serialport_list = []
            portInfo_list =list(serial.tools.list_ports.comports())
            if len(portInfo_list) <=0:
                print("can not find any serial port!")
            else:
                print(portInfo_list)
                for i in range(len(portInfo_list)):
                    plist =list(portInfo_list[i])
                    print(plist)
                    serialport_list.append(plist[0])
            print(serialport_list)


    def port_open(self):
        if not self.Uart.isOpen():
            self.Uart.open()


    def port_close(self):
        self.Uart.close()


    def port_send(self, data):
        number = self.Uart.write(data)
        return number


    def port_read(self):
        while True:
            data = self.Uart.readline()
            self.message = data
            print(self.message)

