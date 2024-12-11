from tkinter import *
import subprocess
import re

root = Tk()
root.geometry('700x500')

def restart_port():
    data = str(subprocess.run(["sudo","usb_resetter","-l"], capture_output=True).stdout)
    data = data.split("\\n")
    for element in data[:]:
        data.remove(element) if "micro:bit" not in element else None

    venprod_pair = []
    for element in data:
        venprod_pair.append(re.search("[a-z0-9]{4}:[a-z0-9]{4}", element).group())
    
    for pair in venprod_pair:
        result = subprocess.run(['sudo', 'usb_resetter', '-d', pair, '--reset-device'], capture_output=True)
        txtoutput.insert(END,result.stdout)

def showfiles():
    choicebox.delete(0,END)
    data = subprocess.run(["ufs", "ls"], capture_output = True)

    if 'Permission denied' in str(data.stdout):
        txtoutput.insert(END,'Permission denied, fixing automatically\n')
        change_permissions()
        showfiles()
        return
    for index,file in enumerate(str(data.stdout)[2:-3].split()):
        choicebox.insert(index,file)
    txtoutput.insert(END,data.stdout)
    txtoutput.see(END)

def change_permissions():
    txtoutput.insert(END,"Executed sudo chmod 666 /dev/ttyACM0\n")
    txtoutput.see(END)
    subprocess.run(["sudo", "chmod", "666", "/dev/ttyACM0"])

def sudo(arg):

    match arg:
        case 'ttyACM0':
            change_permissions()
        case 'restartport':
            restart_port()

    txtoutput.see(END)

def delexp(arg,index):
    file = choicebox.get(index)
    subprocess.run(['ufs', arg, file], capture_output = True)  
    if arg == 'rm':
        showfiles()

txtoutput = Text(root, height = 20, width = 100, bg = 'black', fg='white')
txtoutput.pack()

b1 = Button(root, text="Show microbit files", command = showfiles, width = 23)
b1.place(x=0, y=350)

b2 = Button(root, text="Change ttyACM0 permissions", command = lambda: sudo('ttyACM0'), width = 23)
b2.place(x=0, y=385)

b3 = Button(root, text="Reconnect microbit", command = lambda: sudo('restartport'), width = 23)
b3.place(x=0, y=420)

b4 = Button(root, text="Export", command = lambda: delexp('get',choicebox.curselection()[0]), width = 7)
b4.place(x=344, y=420)

b5 = Button(root, text="Remove", command = lambda: delexp('rm',choicebox.curselection()[0]), width = 7, bg = 'red')
b5.place(x=344, y=455)

label1 = Label(text="Files stored on microbit")
label1.place(x=540,y=346)
choicebox = Listbox(root)
choicebox.place(x=430, y=365, width=265, height=125)

root.mainloop()