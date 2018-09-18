'''
@author: Alex Gillis
'''
from tkinter import *
from GUI.emailDisplay import emailDisplay

def login(event):
    usr = loginEntry.get()
    psw = passwordEntry.get() 
    root.destroy()   
    display = emailDisplay()
    display.openEmailDisplay(usr,psw)
 
    
root = Tk()
root.title("MyEmail Login")
root.geometry("500x500")

frame = Frame(root)

headingTxt = StringVar()
usernameTxt = StringVar()
passwordTxt = StringVar()
headingLabel = Label(frame, textvariable=headingTxt)
usrLabel = Label(frame, textvariable=usernameTxt)
pswdLabel = Label(frame,textvariable=passwordTxt)

button = Button(frame, text="Login")
button.bind("<Button-1>", login)

loginEntry = Entry(frame)
passwordEntry = Entry(frame, show="*")

headingTxt.set("MyEmail Reader")
usernameTxt.set("Username:")
passwordTxt.set("Password:")

headingLabel.pack()
frame.pack()
usrLabel.pack()
loginEntry.pack()
pswdLabel.pack()
passwordEntry.pack()
button.pack()

root.mainloop()