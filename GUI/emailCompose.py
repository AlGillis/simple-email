'''

@author: Alex Gillis
'''
from tkinter import *
from MyEmail import send_email
class emailCompose(object):

    def __init__(self,usr,pws):
        self.root = Tk()
        self.root.title("Compose Email")
        self.root.geometry("500x500")
        
        Label(self.root,text="To:").pack()
        self.toEntry = Entry(self.root, width=20)
        self.toEntry.pack()
        
        Label(self.root,text="From:").pack()
        self.fromEntry = Entry(self.root, width=20)
        self.fromEntry.pack()
        
        Label(self.root,text="Subject:").pack()
        self.subjectEntry = Entry(self.root, width=20)
        self.subjectEntry.pack()
        
        Label(self.root,text="Body:").pack()
        self.bodyEntry = Text(self.root, width=60, height=20)
        self.bodyEntry.pack()
        
        self.usr = usr
        self.pws = pws
        self.sendBtn = Button(self.root, text="Send")
        self.sendBtn.bind("<Button-1>", self.sendEmail)
        self.sendBtn.pack()
        
        self.root.mainloop()
    
    def sendEmail(self, event):
        to = self.toEntry.get()
        frm = self.fromEntry.get()
        subject = self.subjectEntry.get()
        body = self.bodyEntry.get("1.0",END)
        
        sender = send_email.send_email(to,frm,subject,body,self.usr,self.pws)
        sender.sendMail()
        self.root.destroy()

        
        
        
        
        
        