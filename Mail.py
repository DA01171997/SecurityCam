import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

class Mail:
    def __init__(self, senderEmail, password=None):
        self.senderEmail=senderEmail
        self.password=password
        self.receiverEmail=None
        self.subjectHeader=None
        self.plainTextMessage=None
        self.emailAttachment=[]
        
    def addReceiver(self, receiverEmail=None):
        if receiverEmail==None:
            self.receiverEmail = input("Enter receiver email -> ")
        else:
            self.receiverEmail = receiverEmail

    def addSubjectHeader(self,subjectHeader=None):
        if subjectHeader ==None:
            self.subjectHeader = input("Enter subject header -> ")
        else:
            self.subjectHeader = subjectHeader

    def addPlainTextBody(self,plainTextMessage=None):
        if plainTextMessage ==None:
            self.plainTextMessage=input("Enter body message -> ")
        else:
            self.plainTextMessage=plainTextMessage
    
    def addAttachment(self, fileName=None):
        if fileName ==None:
            fileName = input("Enter name of the attachment file -> ")
        if os.path.isfile(fileName):
            self.emailAttachment.append = fileName
        else:
            print("Error: addAttachment : "+fileName+" doesn't exists.")

    def constructNSendMail(self):
        
        #check for necessary components
        #else get it
        if self.receiverEmail==None:
            self.addReceiver()
        if self.subjectHeader==None:
            self.addSubjectHeader()
        if self.plainTextMessage==None:
            self.addPlainTextBody()
        if self.password==None:
            password = input("Enter email password -> ")

        #creat mail object
        self.mail = MIMEMultipart()
        self.mail["From"] = self.senderEmail
        self.mail["To"] = self.receiverEmail
        self.mail["Subject"] = self.subjectHeader
        self.mail["Bcc"] = self.receiverEmail

        #attach the plain text
        self.mail.attach(MIMEText(self.addPlainTextBody), "plain")

        # #add attachment any attachment
        # if len(self.emailattachment) > 0:
        #     for filename in self.emailattachment:
        #         with open(filename, "rb") as file:
        #             attachment = mimebase("application", "octet-stream")
        #             attachment.set_payload(file.read())
        #         encoders.encode_base64(attachment)
        #         attachment.add_header(
        #             "content-disposition",
        #             "attachment; filename = {}".format(filename)
        #         )
        #         self.mail.attach(attachment)
        
        #convert message to string
        message = self.mail.as_string()
        mailServer="smtp.gmail.com"
        serverPortNum = 465
        
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(mailServer,serverPortNum,context=context) as serverConn:
            serverConn.login(self.senderEmail,password)
            serverConn.senderEmail(
                self.senderEmail, self.receiverEmail, message
            )

        



def main():
    mail = Mail("smartCamSender2019@gmail.com","verysecurepassword")
    mail.addReceiver("smartCamReceiver2019@gmail.com")
    mail.addSubjectHeader("TestHeader1")
    mail.addPlainTextBody("TestBody1")
    mail.constructNSendMail()

main()