# RPi-GATT
If you have problem about testing your deivce's ble function. the project will Help you test your device that contains BLE function.

A simple tool project with serial-tool communication using your Raspberry PI and python. 
the tool applied gatt and serial interface to communicate with your device.

## Prerequisites

These have some tools you need to pick up.

### HW
- Raspberry Pi 3/4 *1

- Serial devices *2

- cable *1

![圖片1](https://user-images.githubusercontent.com/22633988/151592999-24036417-2da4-4710-91cf-d2caafe2976b.png)


## Installation
in your Raspberry

`sudo pip3 install gatt`

`sudo apt-get install python3-dbus`

`sudo apt-get install blueman`

and please following [gatt-python](https://github.com/getsenic/gatt-python).



## Usage
### pre-condition

First time you need to connect your DUT by raspberryPi **bluetoothctl** 

These instructions
**step :**
RPi connect to DUT with system
1. open terminal
2. `sudo bluetoothctl`
3. `scan on`
4. `scan off`
5. `connect [MACaddress]`
6. [enter passkey] or not
7. reboot your system and devices.
8. open this project 
9. cd RPi-GATT
10. `python3 main.py`

## Note

### pre-write

previous showing the uuids information when connect to DUT.

you can take the uuids information to write into the `ProjectUUID.py` file. 

`

     def device1(self):
     
        self.service = '0000xxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'         
        self.chara1 = '0000xxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'         
        self.chara2 = '0000xxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'         
        self.chara3 = '0000xxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'
        
`

### communication format

the format of communication :
------ASCII------
- choose your project uuid
       `b0 p [project]`
- connect to yourdevice
      `b0 c [macaddress]`
- enter data to characteristic
     `b0 w [characteristic][data]`


## REFERENCES
the project I reference [gatt-python](https://github.com/getsenic/gatt-python) there contains example code and GATT SDK.

