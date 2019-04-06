from ScoreRecorder import PersonRecord,Data
from tkinter import Entry,Text,StringVar,Tk,END,BOTH

class myEntry(Entry):
    def __init__(self,parent=None,**config):
        Entry.__init__(self,parent,**config)
        self.var=StringVar()
        self.config(textvariable=self.var)
        #self.var.trace_add(("read","write"),self.dealEntry)
    


class myDisplayText(Text):
    def __init__(self,parent=None,**config):
        Text.__init__(self,parent,**config)
        self.scoreIndex="None"
        self.insert('1.0',"Use !set to set which week you want to update.")

    def docommand(self,commands,d):
        com=commands.split(' ')
        if com[0]=="!show":
            if com[1]=='-a':
                self.cleanAll()
                self.insert('1.0',d.displayAll())
            if com[1].isdigit():
                self.cleanAll()
                self.insert('1.0',d.getPerson(com[1]))
        if com[0]=="!q":
            d.save()
            self.quit()
        if com[0]=="!set":
            if len(com)<2 or com[1] not in d.validScoresIndex:
                self.cleanAll()
                self.insert('1.0',"Set has inappropriate parameters, Enter:\n %s" % d.validScoresIndex)
            else:
                self.scoreIndex=com[1]
                self.cleanAll()
                self.insert('1.0',"Week has set to % s" % self.scoreIndex)
        if com[0]=="!write":
            if len(com)<2:
                d.writeXlsx()
            else:
                d.writeXlsx(com[1])
        if com[0]=="!read":
            try:
                d.excelFileName
            except AttributeError:
                d.readXlsxFromString(com[1:])
                return
            try:
                d.writeXlsx()
            except:
                print("unable to write")
                raise 
            d.wipeAllData()
            d.readXlsxFromString(com[1:])
            

        if com[0] in d.db.keys():
            try:
                self.updateData(com,d)
            except KeyError:
                self.cleanAll()
                self.insert('1.0',"\n Current weeks is %s. Remember to set weeks before you start upload." % self.scoreIndex)
            d.save()
    
    def updateData(self,com,d):
        if len(com)==1 or com[1]=="":
            value='B'
            d.updatePersonScore(com[0],self.scoreIndex,'B')
        else:
            value=com[1]
            if com[1][0] in 'ABCD':
                d.updatePersonScore(com[0],self.scoreIndex,value)
            elif value.isdigit() and -1< int(value) < 101:
                d.updatePersonScore(com[0],self.scoreIndex,value)
            else:
                self.cleanAll()
                self.insert('1.0',"Enter A,B,C,D or a number between 0 and 100.")
                return
        self.cleanAll()
        self.insert('1.0',"%s\t%s's %s score set to %s" % (com[0],d.getPerson(com[0]).name,self.scoreIndex,value))
    
    def dealInput(self,ent1: Entry,var,d):
        self.cleanAll()
        s=var.get()
        if len(s) and s[0]=='!':
            self.insert('1.0',"Status:\n")
            commandString='''

Command Mode
-------------------------------------
set <weeks>         set which weeks you want to update   

show -a             display all person data.

show <personKey>    display one person.

write <fileName>    write data to <fileName>

q                   save and quit.

Dangerious Zone
-------------------------------------
read <fileName> rowBegin rowEnd name idkey classes weekScores testScores mScores fScores
                    read data from <fileName>. Notice that weekScores and testScores is list.
                    This command will create backup.xlsx file to save current data, and then 
                    clean all data.
                    eg: 02.xlsx 6 167 4 3 5 [11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28] [29,30,31,32] 8 9
                    CAUTION! It will take a lot of time. and It will wipe all data nomatter
                    success or not
            '''
            commandString="Current weeks is %s" % self.scoreIndex + commandString
            self.insert(END,commandString)

        # Guess person's ID
        test=s.split(' ')
        if len(test[0]) and test[0][0]!='!':
            data=[key for key in d.db.keys() if test[0] in key]
            if 1< len(data) < 10:
                strs=""
                n=0
                for key in data:
                    strs+=str(n)+":  "+"\t".join((key,d.getPerson(key).name))+"\n"
                    n+=1
                self.cleanAll()
                self.insert("1.0",strs)
                if len(test) >1 and test[1].isdigit() and -1 < int(test[1]) <len(data):
                    index=int(test[1])
                    ent1.delete(0,END)
                    ent1.insert(0,data[index])
                    self.cleanAll()
                    self.insert("1.0","\t".join((data[index],d.getPerson(data[index]).name)))
            if len(data)==1:
                self.cleanAll()
                self.insert("1.0","\t".join((data[0],d.getPerson(data[0]).name)))
            
                


    
    def cleanAll(self):
        self.delete('1.0',END)

d=Data()
#print(d.displayAll())



root=Tk()
root.title("ScoreRecorder")

ent1=myEntry(root)
ent1.pack(fill=BOTH)
ent1.config(width=130)
ent1.focus()

text=myDisplayText(root)
text.pack(fill=BOTH)
text.config(height=30)

def display(*argv):
    text.dealInput(ent1,ent1.var,d)

ent1.var.trace_add("write",display)

def docommand(*argv):
    command=ent1.var.get()
    ent1.var.set('')
    text.docommand(command,d)

ent1.bind('<Return>',docommand)


root.mainloop()