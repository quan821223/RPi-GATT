# RPi-GATT
If you have problem about testing your deivce's ble function. the project will Help you test your device that contains BLE function.

## Prerequisites

These have some tools you need to pick up.

### HW
Raspberry Pi 3/4 *1

Serial devices *2

cable *1

the instruction
![圖片1](https://user-images.githubusercontent.com/22633988/151558605-51e352b3-ac64-432d-9b29-118bb4ec9f77.png)


## Installation
in your Raspberry

`sudo pip3 install gatt`

`sudo apt-get install python3-dbus`

## Usage
### pre-condition

First time you need to connect your DUT by raspberryPi **bluetoothctl**

**step :**

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


## REFERENCES
the project I am reference https://github.com/getsenic/gatt-python there contains example code and GATT SDK.

