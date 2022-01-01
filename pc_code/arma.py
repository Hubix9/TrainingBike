import sys, time
import usb # 1.0 not 0.4
import keyboard

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

def resetTurning():
    keyboard.release("a")
    keyboard.release("d")

if __name__ == "__main__":
    theDevice = ArduinoUsbDevice(idVendor=0x16c0, idProduct=0x05df)
    readString = ""
    while True:
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
            resetTurning()
        if controllerValue == 0: 
            resetTurning() 
            keyboard.press("a")
        if controllerValue == 1: 
            resetTurning()
            keyboard.press("d") 
        if int(speedValue) > 0:
            keyboard.press("w")
        else:
            keyboard.release("w")
            

        