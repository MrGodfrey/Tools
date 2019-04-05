from tkinter import *

class Converter:
    def __init__(self, top):
        self.vars = StringVar()
        self.vars.trace('w', self.validate)
        self.Entry1 = Entry(top, textvariable = self.vars,)
        self.Entry1.pack(fill=BOTH,side=TOP)

        self.label=Label(top,textvariable = self.vars)
        self.label.pack()
 
    def validate(self, *args):
        if not self.vars.get().isalpha():
            corrected = ''.join(filter(str.isalpha, self.vars.get()))
            self.vars.set(corrected)
  
root=Tk()
C=Converter(root)
root.mainloop()