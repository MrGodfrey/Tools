from ScoreRecorder import PersonRecord, Data
from tkinter import Entry, Text, StringVar, Tk, END, BOTH


class myEntry(Entry):
    def __init__(self, parent=None, **config):
        Entry.__init__(self, parent, **config)
        self.var = StringVar()
        self.config(textvariable=self.var)
        # self.var.trace_add(("read","write"),self.dealEntry)


class myDisplayText(Text):
    def __init__(self, parent=None, **config):
        Text.__init__(self, parent, **config)
        self.scoreIndex = "None"
        self.insert('1.0', "Use !set to set which week you want to update.")
        self.UPLOAD_URL="http://118.25.210.74:876/upload"
        # local http://127.0.0.1:5000/upload
        # service http://118.25.210.74:876/upload
        

    def readFromFile(self, ent, com, d):
        import _thread as thread
        import time

        def onhold(*argv):
            ent.var.set("")

        def read(com, d):
            exitmutexes = thread.allocate_lock()
            thread.start_new_thread(
                d.readXlsxFromString, (com[1:], exitmutexes))
            n = 0
            traceID = ent.var.trace_add("write", onhold)
            while not exitmutexes.locked():
                self.cleanAll()
                self.insert('1.0', "Wait for reading file. %d s" % n)
                time.sleep(1)
                n += 1
            ent.var.trace_remove("write", traceID)
            self.cleanAll()
            self.insert(
                '1.0', "Finished reading file from %s. \nEnter !show -a to show all data." % com[1])

        try:
            d.excelFileName
        except AttributeError:
            thread.start_new_thread(read, (com, d))
            return
        try:
            d.writeXlsx()
        except:
            self.cleanAll()
            self.insert('1.0',"Unable to write to file. Delete Data.* and try again")
            return
        d.wipeAllData()
        thread.start_new_thread(read, (com, d))

    def docommand(self, ent, commands, d):
        '''
        deal with command. When add new command, remember to check this place.
        '''
        com = commands.split(' ')
        if com[0] == "!show":
            if com[1] == '-a':
                self.cleanAll()
                self.insert('1.0', d.displayAll())
            if com[1].isdigit():
                self.cleanAll()
                self.insert('1.0', d.getPerson(com[1]))
        if com[0] == "!q":
            d.save()
            self.quit()
        if com[0] == "!set":
            if len(com) < 2 or com[1] not in d.validScoresIndex:
                self.cleanAll()
                self.insert(
                    '1.0', "Set has inappropriate parameters, Enter:\n %s" % d.validScoresIndex)
            else:
                self.scoreIndex = com[1]
                self.cleanAll()
                self.insert('1.0', "Week has set to % s" % self.scoreIndex)
        if com[0] == "!write":
            if len(com) < 2:
                d.writeXlsx()
            else:
                d.writeXlsx(com[1])
            self.cleanAll()
            self.insert('1.0', "Data saved!")
        if com[0] == "!read":
            self.readFromFile(ent, com, d)
        if com[0] == "!upload":
            if len(com)>1 and com[1]:
                self.uploadURL(com[1])
            else:
                self.uploadURL(self.UPLOAD_URL)

        if com[0] in d.db.keys():
            try:
                self.updateData(com, d)
            except KeyError:
                self.cleanAll()
                self.insert(
                    '1.0', "\n Current weeks is %s. Remember to set weeks before you start upload." % self.scoreIndex)
            d.save()
    
    def uploadURL(self,s):
        import requests

        files=[{'file':open('Data.dat','rb')},\
            {'file':open('Data.bak','rb')},\
                {'file':open('Data.dir','rb')}]
        self.cleanAll()
        for f in files:
            r=requests.post(s,files=f)
            if 'success' in r.text:
                self.insert(END,"\nUpload %s success." % f['file'].name)
            else:
                self.insert(END,"\nUpload %s failure." % f['file'].name)


    def updateData(self, com, d):
        if len(com) == 1 or com[1] == "":
            value = 'A'
            d.updatePersonScore(com[0], self.scoreIndex, 'A')
        else:
            value = com[1]
            if com[1][0] in 'ABCD':
                d.updatePersonScore(com[0], self.scoreIndex, value[0:2])
            elif value.isdigit() and -1 < int(value) < 101:
                d.updatePersonScore(com[0], self.scoreIndex, value)
            else:
                self.cleanAll()
                self.insert(
                    '1.0', "Enter A,B,C,D or a number between 0 and 100.")
                return
        self.cleanAll()
        self.insert('1.0', "%s\t%s's %s score set to %s" %
                    (com[0], d.getPerson(com[0]).name, self.scoreIndex, value))

    def dealInput(self, ent1: Entry, var, d):
        self.cleanAll()
        s = var.get()
        if len(s) and s[0] == '!':
            self.insert('1.0', "Status:\n")
            commandString = '''

Command Mode
-------------------------------------
set <weeks>         set which weeks you want to update   

show -a             display all person data.

show <personKey>    display one person.

write <fileName>    write data to <fileName>

upload <url>        upload data to url

q                   save and quit.

Dangerous Zone
-------------------------------------
read <fileName> rowBegin rowEnd name idkey classes weekScores testScores mScores fScores
                    read data from <fileName>. Notice that weekScores and testScores is list.
                    This command will create backup.xlsx file to save current data, and then 
                    clean all data.
                    eg: 02.xlsx 6 167 4 3 5 [11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28] [29,30,31,32] 8 9
                    CAUTION! It will take a lot of time. and It will wipe all data nomatter
                    success or not
            '''
            commandString = "Current weeks is %s" % self.scoreIndex + commandString
            self.insert(END, commandString)

        # Guess person's ID
        test = s.split(' ')
        if len(test[0]) and test[0][0] != '!':
            data = [key for key in d.db.keys() if test[0] in key]
            if 1 < len(data) < 10:
                strs = ""
                n = 0
                for key in data:
                    strs += str(n)+":  " + \
                        "\t".join((key, d.getPerson(key).name))+"\n"
                    n += 1
                self.cleanAll()
                self.insert("1.0", strs)
                if len(test) > 1 and test[1].isdigit() and -1 < int(test[1]) < len(data):
                    index = int(test[1])
                    ent1.delete(0, END)
                    ent1.insert(0, data[index])
                    self.cleanAll()
                    self.insert("1.0", "\t".join(
                        (data[index], d.getPerson(data[index]).name)))
            if len(data) == 1:
                self.cleanAll()
                self.insert("1.0", "\t".join(
                    (data[0], d.getPerson(data[0]).name))+"\nUse Tab to complete.")
                
                def wordCompete(event):
                    ent1.delete(0, END)
                    ent1.insert(0, data[0])
                    return "break"
                
                ent1.bind('<Tab>',(lambda e: wordCompete(e))) 
            
                  

    def cleanAll(self):
        self.delete('1.0', END)

class mainFrame:
    def __init__(self,top):
        self.d=Data()

        self.ent1=myEntry(top)
        self.ent1.pack(fill=BOTH)
        self.ent1.config(width=130)
        self.ent1.focus()

        self.ent1.var.trace_add("write", self.display)
        self.ent1.bind('<Return>', self.docommand)

        self.text=myDisplayText(top)
        self.text.pack(fill=BOTH)
        self.text.config(height=30) 
        # don't take focus, you can't use tab to get here.
        self.text.config(takefocus=False)
        # don't do anything
        self.text.bind("<Key>",lambda e:self.__textEvent(e))
    
    def __textEvent(self,event):
        # Control's mask is 0X0004
        if(event.state==0x0004 and event.keysym=='c' ):
            return
        else:
        # can't understand why
            return "break"
    
    def display(self,*argv):
        self.text.dealInput(self.ent1, self.ent1.var, self.d)

    def docommand(self,*argv):
        command = self.ent1.var.get()
        self.ent1.var.set('')
        self.text.docommand(self.ent1, command, self.d)


root = Tk()
root.title("ScoreRecorder")
c=mainFrame(root)
root.mainloop()