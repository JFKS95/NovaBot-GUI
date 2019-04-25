from tkinter import *
import time
import audiofft
import CreateMap
import visualDetection
#import rospy


root = Tk()
#Setting Window Properties
root.geometry('1024x576') #Sets root (GUI) size
root.configure(background='grey')
root.title('Galaxy Observatory System (GOS)')
root.grid_columnconfigure(2, minsize=200)
root.grid_columnconfigure(4, minsize=200)
root.grid_columnconfigure(6, minsize=200)
root.grid_rowconfigure(0, minsize=40)
root.grid_rowconfigure(1, minsize=40)
root.grid_rowconfigure(2, minsize=40)
root.grid_rowconfigure(3, minsize=40)
root.grid_rowconfigure(4, minsize=40)
root.grid_rowconfigure(5, minsize=40)
root.grid_rowconfigure(6, minsize=40)
root.grid_rowconfigure(7, minsize=40)
root.grid_rowconfigure(8, minsize=40)
root.grid_rowconfigure(9, minsize=40)
root.grid_rowconfigure(10, minsize=40)
root.grid_rowconfigure(11, minsize=40)
root.grid_rowconfigure(12, minsize=40)


#Define variables
V = IntVar()
V.set(1) #Sets Manual as first default
#Mission Info Labels
label_1 = Label(root, text="Mission Information Panel", bg='grey', font='bold')
label_2 = Label(root, text="Mission Time", bg='grey')
label_3 = Label(root, text="Mission Phase", bg='grey')
label_4 = Label(root, text="NOVA Bot Speed", bg='grey')
label_5 = Label(root, text="Battery", bg='grey')
label_6 = Label(root, text="Signal", bg='grey')
label_7 = Label(root, text="Audio Recording", bg='grey')

#Control Panel Labels
label_8 = Label(root, text="Control Panel", bg='grey', font='bold')
label_9 = Label(root, text="Control Mode", bg='grey')
label_10 = Label(root, text="Select Mission Phase", bg='grey')
#Tactical Panel Lables
label_11 = Label(root, text="Tactical Panel", bg='grey', font='bold')
label_12 = Label(root, text="Audio Error Code", bg='grey')
label_12b = Label(root, text="Visual Error Code", bg='grey')
label_13 = Label(root, text="Shutdown Zone", bg='grey')

#Replace these entries with mission data
entry_2 = Entry(root)
entry_2.insert(0, "Time elapsed")
entry_3 = Entry(root)
entry_3.insert(0, "Mission Phase 1")
entry_4 = Entry(root)
entry_4.insert(0, "0 Speed")
entry_5 = Entry(root)
entry_5.insert(0, "Not Available")
entry_6 = Entry(root)
entry_6.insert(0, "No signal")
entry_7 = Entry(root)
entry_7.insert(0, "OFF")
radiobutton_9a = Radiobutton(root, text="Manual", variable=V, value=1, bg="grey")
radiobutton_9b = Radiobutton(root, text="Partially Autonomous", variable=V, value=2, bg="grey")
entry_10 = Entry(root)
entry_10.insert(0, "I am 10")
entry_12 = Entry(root)
entry_12.insert(0, "I am 12")
entry_13 = Entry(root)
entry_13.insert(0, "I am 13")
entry_14 = Entry(root)
entry_14.insert(0, "I am 14")

#Control Panel Buttons
button_0 = Button(root, text="Power Up", bg="Light Green", fg="Black", height='2', width='10', font="bold")
button_1 = Button(root, text="RTB", bg="Yellow", fg="Black", height='2', width='7')
button_2 = Button(root, text="Reset", bg="Orange", fg="Black", height='2', width='7')
button_3 = Button(root, text="Shutdown", bg="Dark Red", fg="White", height='2', width='10', font="bold")
button_4 = Button(root, text="Accept", bg="Light Green")
button_5 = Button(root, text="Reject", bg="Dark Red", fg="White")
button_6 = Button(root, text="Record Audio", bg="Light Blue", fg="Black", height='1', width='15')
button_7 = Button(root, text="Scan Environment", bg="Light Blue", fg="Black", height='1', width='15')
button_8 = Button(root, text="Record Visual", bg="Light Blue", fg="Black", height='1', width='15')
button_9 = Button(root, text="Droid Shutdown", bg="Light Blue", fg="Black", height='1', width='15')

#Binding Commands to Buttons
def PowerUp(event):
    print("NOVA Bot Powering Up") #Replace with the On Command
button_0.bind("<Button-1>", PowerUp)
def RTB(event):
    print("NOVA Bot Returning to Base") #Replace with the RTB Command
button_1.bind("<Button-1>", RTB)
def Reset(event):
    print("NOVA Bot Reset") #Replace with the RESET Command
button_2.bind("<Button-1>", Reset)
def Shutdown(event):
    print("NOVA Bot Shutdown") #Replace with the SHUTDOWN Command
button_3.bind("<Button-1>", Shutdown)
def AudioProcess(event):
    entry_7.delete(0,END)
    entry_7.insert(0, "ON")
    entry_7.get()
    
    data = audiofft.stream()
    errorCode = audiofft.run(data)
    
    entry_7.delete(0,END)
    entry_7.insert(0, "OFF")
    entry_7.get()

    entry_12.delete(0, END)
    entry_12.insert(0, errorCode)
button_6.bind("<Button-1>", AudioProcess)

def MazeProcess(event):

    CreateMap.run()
button_7.bind("<Button-1>", MazeProcess)

def VisualProcess(event):

    vcode = visualDetection.run()

    entry_14.delete(0, END)
    entry_14.insert(0, vcode)
    
button_8.bind("<Button-1>", VisualProcess)

def ManualSelection(event):
    print("Manual Control selected") #Replace with the Manual Selection Command
radiobutton_9a.bind("<Button-1>", ManualSelection)
def AutoSelection(event):
    print("Partially Autonomous Control selected") #Replace with the Partially Autonomous Selection Command
radiobutton_9b.bind("<Button-1>", AutoSelection)

#Grid layout - Labels
label_1.grid(row=0, column=0, columnspan=2)
label_2.grid(row=1, column=0, sticky=E)
label_3.grid(row=2, column=0, sticky=E)
label_4.grid(row=3, column=0, sticky=E)
label_5.grid(row=4, column=0, sticky=E) #Sticky=E = align east (right)
label_6.grid(row=5, column=0, sticky=E)
label_7.grid(row=6, column=0, sticky=E)
label_8.grid(row=0, column=2, columnspan=3)
label_9.grid(row=1, column=2, sticky=E)
label_10.grid(row=3, column=2, sticky=E)
label_11.grid(row=0, column=4, columnspan=6)
label_12.grid(row=2, column=4, sticky=E)
label_12b.grid(row=1, column=4, sticky=E)
label_13.grid(row=4, column=4, sticky=E)

#Grid layout - Data to display
entry_2.grid(row=1, column=1)
entry_3.grid(row=2, column=1)
entry_4.grid(row=3, column=1)
entry_5.grid(row=4, column=1)
entry_6.grid(row=5, column=1)
entry_7.grid(row=6, column=1)
radiobutton_9a.grid(row=1, column=3)
radiobutton_9b.grid(row=2, column=3)
entry_10.grid(row=3, column=3)
entry_12.grid(row=2, column=5)
entry_13.grid(row=4, column=5)
entry_14.grid(row=1, column=5)


#Grid layout - Buttons
button_0.grid(row=8, column=1,)
button_1.grid(row=4, column=3, sticky=W)
button_2.grid(row=4, column=3, sticky=E)
button_3.grid(row=8, column=5)
button_4.grid(row=3, column=5, sticky=W)
button_5.grid(row=3, column=5, sticky=E)
button_6.grid(row=8, column=3)
button_7.grid(row=6, column=3)
button_8.grid(row=7, column=3)
button_9.grid(row=9, column=3)

root.mainloop()
