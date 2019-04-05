from ScoreRecorder import PersonRecord,Data
from tkinter import *

class myEntry(Entry):
    def __init__(self,parent=None,**config):
        Entry.__init__(self,parent,**config)
        self.var=StringVar()
        self.config(textvariable=self.var)
        #self.var.trace_add(("read","write"),self.dealEntry)
    


class myDisplayText(Text):
    def __init__(self,parent=None,**config):
        Text.__init__(self,parent,**config)

    def docommand(self,commands,d):
        com=commands.split(' ')
        if com[0]=="show":
            if com[1]=='-a':
                self.cleanAll()
                self.insert('1.0',d.displayAll())
            if com[1].isdigit():
                self.cleanAll()
                self.insert('1.0',d.getPerson(com[1]))
    
    def dealInput(self,var):
        self.cleanAll()
        helpstring="""
        你可以输入 show -a
        """
        self.insert('1.0',helpstring)
        
    
    def cleanAll(self):
        self.delete('1.0',END)

d=Data()
#print(d.displayAll())

root=Tk()
root.title("ScoreRecorder")

ent1=myEntry(root)
ent1.pack(fill=BOTH)

text=myDisplayText(root)
text.pack(fill=BOTH)

def display(*argv):
    text.dealInput(ent1.var)

ent1.var.trace_add("write",display)

def docommand(*argv):
    command=ent1.var.get()
    ent1.var.set('')
    text.docommand(command,d)

ent1.bind('<Return>',docommand)






root.mainloop()