'''

@author: Alex Gillis

'''
from tkinter import *
from MyEmail import read_email
from GUI import emailCompose

class emailDisplay:
    def openEmailDisplay(self, usr,psw):
        self.root = Tk()
        self.root.title("MyEmail Display")
        self.root.geometry("1000x700")
        self.bodyDisplay = Text(self.root)
        
        self.lb = Listbox(self.root, name='lb', width='120',height='15')
        self.lb.bind('<<ListboxSelect>>', self.openEmailBody)

        self.emailReader = read_email.read_email(usr,psw)
        self.emailReader.connect_to_server()
        self.emailReader.process_mailbox()      
        self.buildDisplay()
        self.usr = usr
        self.psw = psw
        self.lb.pack()
        self.root.mainloop()
            
    def onselect(self,evt):
        # Note here that Tkinter passes an event object to onselect()
        w = evt.widget
        index = int(w.curselection()[0])
        value = w.get(index)
        print('You selected item %d: "%s"' % (index, value))
    
    def buildDisplay(self):
        heading = Label(self.root, text="Inbox")
        
        composeEmailBtn = Button(self.root, text="Compose Email")
        composeEmailBtn.bind("<Button-1>", self.composeEmail)
        heading.pack()
        composeEmailBtn.pack(side=BOTTOM)
        
        for i,mail in enumerate(self.emailReader.emails):
            headers = mail[0]
            subjectField = self.emailReader.getSubjectHeader(headers)[1]
            toField = self.emailReader.getToHeader(headers)[1]
            fromField = self.emailReader.getFromHeader(headers)[1]
            dateField = self.emailReader.getDateHeader(headers)[1] 
            
            rowTxt = "Subject: "+ subjectField + " | To: " + toField + " | From: " + fromField + " | Date: " + dateField
            self.lb.insert(i,rowTxt)

    #Event Handler for Row Button      
    def openEmailBody(self, event):
        if(self.bodyDisplay):
            self.bodyDisplay.destroy()
        
        w = event.widget
        index = int(w.curselection()[0])
        rowTxt = w.get(index)
        date = rowTxt.split("Date: ",1)[1]
        bodyArry = self.emailReader.getBodyFromDate(date)[1:]
        bodyStr = ""
        for t in bodyArry:
            bodyStr += t
        bodyTxt = StringVar()
        bodyTxt.set(bodyStr)
        self.bodyDisplay = Text(self.root)
        self.bodyDisplay.insert(END, bodyStr)
        self.bodyDisplay.pack()
        print(bodyTxt)
        
    def composeEmail(self, event):
        emailCompose.emailCompose(self.usr,self.psw)
        