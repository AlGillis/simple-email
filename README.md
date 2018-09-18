# simple-email

* Term project for CS 4759 Computer Networks

## Overview

This is a simple email client. The program allows a user to send and receive plain text emails over SMTP, which requires the creation and parsing of SMTP communications. A user interacts with the program through a GUI. It does not use any preexisting libraries to handle the SMTP communications. However, preexisting libraries are used to handle MIME formatting and SSL connections.

In addition, the program uses a readily available email servers, Gmail. When sending an email, the program establishes an SSL connection with the email server. It then sends the appropriate commands and message to the email server. To receive messages, an SSL connection is established with the email server, and all the email data is given to the client from the server. The client then must parse the data received from the server.  


## Tools

Language: Python
<br><br>
Packages: 
* Tkinter – The creation of the GUI
* Imaplib – Used to establish the SSL connection to the email server
* MIMEText – Formats a message to MIME


## References

* RFC 821
* RFC 2821
* RFC 2822
