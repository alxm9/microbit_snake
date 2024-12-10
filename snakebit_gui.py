from tkinter import *
import os
import subprocess
import serial
import time
import re

root = Tk()
root.geometry('700x500')

def scan():

    txtoutput.insert(END,'---------\n')
    data = subprocess.run(["ufs", "ls"], capture_output = True)
    txtoutput.insert(END,data.stdout)

def sudo(arg):

    match arg:

        case 'openport':
            subprocess.run(["sudo", "chmod", "666", "/dev/ttyACM0"])

        case 'restartport':
            data = str(subprocess.run(["sudo","usb_resetter","-l"], capture_output=True).stdout)
            data = data.split("\\n")
            for element in data[:]:
                data.remove(element) if "micro:bit" not in element else None

            venprod_pair = []
            for element in data:
                venprod_pair.append(re.search("[a-z0-9]{4}:[a-z0-9]{4}", element).group())
            
            for pair in venprod_pair:
                result = subprocess.run(['sudo', 'usb_resetter'], capture_output=True)

            # serial.Serial("/dev/ttyACM0", 9600).close()
            # time.sleep(4)
            # serial.Serial("/dev/ttyACM0",9600)
            # print('here')

txtoutput = Text(root, height = 20, width = 100)
txtoutput.pack()

b1 = Button(root, text="Scan microbit", command = scan)
b1.pack()

b2 = Button(root, text="sudo chmod 666 /dev/ttyACM0", command = lambda: sudo('openport'))
b2.pack()

b3 = Button(root, text="Reconnect microbit", command = lambda: sudo('restartport'))
b3.pack()

root.mainloop()