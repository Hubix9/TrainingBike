from re import T
import sys, time
import usb # 1.0 not 0.4
import keyboard
import pyvjoy
import time

sys.path.append("..")

from arduino.usbdevice import ArduinoUsbDevice

def checkForData():
        global theDevice, readString
        try:
            charRead = chr(theDevice.read())
            readString = readString + charRead
            #time.sleep(0.010)
        except:
            # TODO: Check for exception properly
            #print("failed reading")
            time.sleep(0.100)


controllerValue = 0
speedValue = 0

def resetTurning(j): 
    j.set_axis(pyvjoy.HID_USAGE_Y, 0x4000)
    

if __name__ == "__main__": 
    theDevice = ArduinoUsbDevice(idVendor=0x16c0, idProduct=0x05df)
    joystick = pyvjoy.VJoyDevice(1)
    readString = ""
    while True:
        #Buttons 
        buttons = [[],[False,"c"],[False, "y"],[False, "u"],[False, "i"]]
        for i in range(1,5,1):
            if keyboard.is_pressed(buttons[i][1]):
                if buttons[i][0] == False:
                    joystick.set_button(i, 1)
                    buttons[i][0] = True
            else:
                if buttons[i][0] == True:
                    joystick.set_button(i, 0)
                    buttons[i][0] = False


        
        if keyboard.is_pressed("x"):
            break
        checkForData()  
        packets = readString.split("!")
        if len(packets) == 0:
            continue
        packet = packets[-1]
        if len(packet) == 0:
            continue
        print(packet)
        if packet[-1] != '$':
            continue
        packet = packet.split("/")
        controllerValue = int(packet[0])
        speedValue = int(packet[1][:-1])
        print(f"received packet, speed value: {speedValue}, controller value: {controllerValue}")  
        if controllerValue == 2:
            resetTurning(joystick)
        if controllerValue == 0: 
            resetTurning(joystick) 
            joystick.set_axis(pyvjoy.HID_USAGE_Y, 0x1) 
        if controllerValue == 1: 
            resetTurning(joystick)
            joystick.set_axis(pyvjoy.HID_USAGE_Y, 0x8000) 
        if int(speedValue) > 0:
            joystick.set_axis(pyvjoy.HID_USAGE_X, round(0x8000 * (speedValue / 30)))
        else:
            joystick.set_axis(pyvjoy.HID_USAGE_X, 0x1)
        
            

        