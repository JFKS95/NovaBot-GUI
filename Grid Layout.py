from tkinter import *

root = Tk()

root.geometry('1024x576') #Sets root (GUI) size

#Creating basic password entry
label_1 = Label(root, text="Name")
label_2 = Label(root, text="Password")
entry_1 = Entry(root)
entry_2 = Entry(root)
button_1 = Button(root, text="Submit", bg="green", fg="black")

#Creating a grid layout (rows and columns as opposed to packing)
label_1.grid(row=0, sticky=E)
label_2.grid(row=1, sticky=E)    #Sticky=E = align east (right)

entry_1.grid(row=0, column=1)
entry_2.grid(row=1, column=1)

c = Checkbutton(root, text="Keep me logged in")
c.grid(row=2, columnspan=2) #Checkbox and lable merges two columns

button_1.grid(row=3)

root.mainloop()