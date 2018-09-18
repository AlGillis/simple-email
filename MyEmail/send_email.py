'''

@author: Alex Gillis
'''
from email.mime.text import MIMEText
import ssl
import socket
from email.base64mime import body_encode as encode_base64
import re

class send_email(object):

    def __init__(self,to,frm,subject,body,usr,pwd):
        self.to = to
        self.frm = frm
        self.subject = subject 
        self.body = body
        self.timeout = socket._GLOBAL_DEFAULT_TIMEOUT
        self.host = 'smtp.gmail.com'  # smtp.mail.yahoo.com
        self.port = 465
        self.bCRLF = str.encode("\r\n")
        self.CRLF = "\r\n"
        self.usr = usr
        self.pwd = pwd
        self.createMessage()
       
    def createMessage(self):
        self.msg = MIMEText(self.body)
        self.msg['Subject'] = self.subject
        self.msg['From'] = self.frm
        self.msg['To'] = self.to
        
    def sendMail(self):
        host = self.host
        port = self.port
        timeout = self.timeout
        username = self.usr
        password = self.pwd
        msg = self.msg
        bCRLF = self.bCRLF
        
        context = ssl._create_stdlib_context(certfile=None, keyfile=None)
        sock = socket.create_connection((host, port), timeout, None)
        sock = context.wrap_socket(sock, server_hostname=host)
        
        code,mssg = self.serverResponse(sock)
        print("REPLY: " + str(code) + " " + str(mssg))
        
        #Command:  ehlo [addr]\r\n
        #Usr Address
        host = socket.gethostname()
        addr = socket.gethostbyname(host)
        addr = "[{}]".format(addr)
         
        s = "ehlo {}\r\n".format(addr)
        s = str.encode(s)
         
        self.send(s,sock)
        
            
        #AUTH
        loginInfo = self.auth_info(username, password)
        response = encode_base64(loginInfo.encode('ascii'), eol='')
        cmd = "AUTH PLAIN " + response + self.CRLF
        cmd = str.encode(cmd)
          
        self.send(cmd,sock)
         
         
        #SENDING
        
        cmd = "mail FROM:<{}> size=204{}".format(self.frm,self.CRLF)
        cmd = str.encode(cmd)
        self.send(cmd,sock)
        
        cmd = "rcpt TO:<{}>{}".format(self.to,self.CRLF)
        cmd = str.encode(cmd)
        self.send(cmd,sock)
         
        cmd = "data{}".format(self.CRLF)
        cmd = str.encode(cmd)
        self.send(cmd,sock)
        
        msg = msg.as_string()
        msg =self. _fix_eols(msg).encode('ascii')
        q = self._quote_periods(msg)
        if q[-2:] != bCRLF:
            q = q + bCRLF
        q = q + b"." + bCRLF
        self.send(q,sock)
        
        cmd = "quit{}".format(self.CRLF)
        self.send(str.encode(cmd),sock)
    def send(self,cmd, sock):
        print(cmd)
        try:
            sock.sendall(cmd)
            code,msg = self.serverResponse(sock)
            print("REPLY: " + str(code) + " " + str(msg))
        except OSError:
            print('Server not connected')
            
    
    def auth_info(self,user,password):
        return "\0%s\0%s" % (user, password)
    def _fix_eols(self,data):
        return  re.sub(r'(?:\r\n|\n|\r(?!\n))', '\r\n', data)
    def _quote_periods(self,bindata):
        return re.sub(br'(?m)^\.', b'..', bindata)
    
    def serverResponse(self,sock):
        _MAXLINE = 8192
        resp = []
        afile = sock.makefile('rb')
        while 1:
            try:
                line = afile.readline(_MAXLINE + 1)
            except OSError:
                print("ERROR")
            if not line:
                print("ERROR")
    
            resp.append(line[4:].strip(b' \t\r\n'))
            code = line[:3]
            # Don't attempt to read a continuation line if error incorrect.
            try:
                errcode = int(code)
            except ValueError:
                errcode = -1
                break
            # Check if multiline response.
            if line[3:4] != b"-":
                break
        errmsg = b"\n".join(resp)
        return errcode, errmsg
        