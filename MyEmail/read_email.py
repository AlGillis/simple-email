'''
@author: Alex Gillis
'''

import re
import sys
import imaplib
from io import StringIO


class read_email():
    EMAIL_ACCOUNT = ""
    
    headerREGEX = re.compile(r'^(From |[\041-\071\073-\176]*:|[\t ])')
    
    EMAIL_FOLDER = "INBOX"
    Pass = ""
    
    def __init__(self,acct,psw):
        self.EMAIL_ACCOUNT = acct
        self.Pass = psw
        self.M = imaplib.IMAP4_SSL('imap.gmail.com')
        self.emails = []
        
    def connect_to_server(self):

        try:
            rv, data = self.M.login(self.EMAIL_ACCOUNT, self.Pass)
        except imaplib.IMAP4.error:
            print ("Login Unsuccessful ")
            sys.exit(1)
        
        print(rv, data)

        rv, data = self.M.select(self.EMAIL_FOLDER)
        if rv == 'OK':
            print(rv)
        else:
            print("ERROR: Unable to open mailbox ", rv)
        
        
    def process_mailbox(self):
        rv, data = self.M.search(None, "ALL")
        if rv != 'OK':
            print("ERROR: No messages found!")
            return
    
        for num in data[0].split():
            rv, data = self.M.fetch(num, '(RFC822)')
            if rv != 'OK':
                print("ERROR: Message fetch failed", num)
                return
            
            raw_email = data[0][1]
            #Decode from bytes to raw utf-8 string
            raw_email_string = raw_email.decode('utf-8')
            
            emailFile = StringIO(raw_email_string)
            lines = emailFile.readlines()
            
            headers = []
            body = []
            lastheader = ''
            lastvalue = []

            for line in lines:
                #Searching for a line that doesn't match the RFC 2822
                if not self.headerREGEX.match(line):
                    #Body of the MyEmail
                    body.append(line)
                    continue
                if line[0] in ' \t':
                    lastvalue.append(line)
                    continue 
                i = line.find(':')
                lastheader = line[:i]
                lastvalue = [line]
                if lastheader:
                    name, value = lastvalue[0].split(':', 1)
                    value = value.lstrip(' \t') + ''.join(lastvalue[1:])
                    value = value.rstrip('\r\n')
                    headers.append((name,value))
                    
            self.emails.append((headers,body))
        self.M.close()
        self.M.logout()
    
    def getSubjectHeader(self,mail):
        header = ()
        for h in mail:
            if "Subject" in h[0]:
                header = h
        return header
    def getToHeader(self,mail):
        header = ()
        for h in mail:
            if "To" in h[0]:
                header = h
        return header
    def getFromHeader(self,mail):
        header = ()
        for h in mail:
            if "From" in h[0]:
                header = h
        return header
    def getDateHeader(self,mail):
        header = ()
        for h in mail:
            if "Date" in h[0]:
                header = h
        return header
    def getBodyFromDate(self,date):
        body = ""
        for email in self.emails:
            for headers in email[0]:  
                if date in headers[1]:
                    body = email[1]
                    break
        return body