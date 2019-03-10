from tkinter import *

root = Tk()
#Creating text as labels
theLabel = Label(root, text="Welcome to the Galaxy Observatory System")
theLabel.pack()
#Organising the layout
topframe = Frame(root)
topframe.pack(side=TOP)
bottomframe = Frame(root)
bottomframe.pack(side=BOTTOM)
#Creating button widgets
button1 = Button(topframe, text='Button 1', fg='red')
button2 = Button(topframe, text='Button 2', fg='blue')
button3 = Button(topframe, text='Button 3', fg='green')
#Displaying buttons
button1.pack(side=LEFT)
button2.pack(side=LEFT)
button3.pack(side=LEFT)

#Text Entry
label_1 = Label(bottomframe, text='Name')
label_2 = Label(bottomframe, text='Password')
entry_1 = Entry(root)
entry_2 = Entry(root)
#Displaying the Entries
label_1.pack(side=LEFT)
entry_1.pack(side=BOTTOM)
label_2.pack(side=LEFT)
entry_2.pack(side=BOTTOM)

#Binding Functions to a layout.
def Shutdown(event):
    print("NOVA Bot Shutdown")
button4 = Button(bottomframe, text='Shutdown', fg='indigo')
button4.bind("<Button-1>", Shutdown) #Binds button click to function
button4.pack(side=BOTTOM)


root.mainloop() #keeps GUI running