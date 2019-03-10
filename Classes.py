from tkinter import *

class GOSButtons:

    def __init__(self, master): #master=root
        frame = Frame(master)
        frame.pack()

        self.ShutdownButton = Button(frame, text="Shutdown NOVA Bot", command=self.Shutdown)
        self.ShutdownButton.pack(side=LEFT)

        self.QuitButton = Button(frame, text="Quit", command=frame.quit)
        self.QuitButton.pack(side=LEFT)

    def Shutdown(self):
        print("Nova Bot Shutdown")

root = Tk()
b = GOSButtons(root)
root.mainloop()