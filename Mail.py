import email, smtplib, ssl
import os

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import jinja2


class Mail:
    #creating the mail sender
    #password is optional
    #password won't get save if it isn't implicitly
    #set at the time of creation
    def __init__(self, senderEmail, password=None):
        self.senderEmail = senderEmail
        self.password = password
        self.receiverEmail = None
        self.subjectHeader = None
        self.plainTextMessage = None
        self.emailAttachment = []
        template_loader = jinja2.FileSystemLoader(searchpath='./email_templates')
        self.template_env = jinja2.Environment(loader=template_loader)
        self.htmlFlag = True
        self.html = None
        
    #add email of the receiver    
    def addReceiver(self, receiverEmail=None):
        if receiverEmail == None:
            self.receiverEmail = input("Enter receiver email -> ")
        else:
            self.receiverEmail = receiverEmail

    #add subject header for the email
    def addSubjectHeader(self, subjectHeader=None):
        if subjectHeader == None:
            self.subjectHeader = input("Enter subject header -> ")
        else:
            self.subjectHeader = subjectHeader

    #add a plaintext verision for the body of the email
    #if html option is True, also add an HTML Version
    def addBody(self, plainTextMessage=None, html_context=None):
        if plainTextMessage == None:
            self.plainTextMessage = input("Enter body message -> ")
        else:
            self.plainTextMessage = plainTextMessage
        if html_context:
            self.htmlFlag = html_context is None
            template = self.template_env.get_template('detection_alert.jinja')
            self.html = template.render(html_context)
    
    #add attachment to the email by specifying the filename
    #file need to be inside the same folder 
    #or an absolute path is needed
    #email can add multiple attachment
    def addAttachment(self, fileName=None):
        if fileName == None:
            fileName = input("Enter name of the attachment file -> ")
        if os.path.isfile(fileName):
            self.emailAttachment.append(fileName)
        else:
            print("Error: addAttachment : " + fileName + " doesn't exists.")

    
    #compile the email with all the necessary components
    #then send
    def constructNSendMail(self, password=None):

        #check for necessary components
        #else get it
        if self.receiverEmail == None:
            self.addReceiver()
        if self.subjectHeader == None:
            self.addSubjectHeader()
        if self.plainTextMessage == None:
            self.addBody()

        #if password wasn't set at the time of creation
        #password won't get save permenantly
        if self.password == None and password == None:
            password = input("Enter email password -> ")
        if self.password != None and password == None:
            password = self.password

        #create mail object
        mail = MIMEMultipart()
        mail["From"] = self.senderEmail
        mail["To"] = self.receiverEmail
        mail["Subject"] = self.subjectHeader
        mail["Bcc"] = self.receiverEmail

        #attach the plain text
        mail.attach(MIMEText(str(self.plainTextMessage), "plain"))
        
        #attach html verison html is set
        if self.htmlFlag:
            mail.attach(MIMEText(str(self.html), "html"))

        
        #add any attachment that was set
        if len(self.emailAttachment) > 0:
            for fileName in self.emailAttachment:
                with open(fileName, "rb") as file:
                    attachment = MIMEBase("application", "octet-stream")
                    attachment.set_payload(file.read())
                encoders.encode_base64(attachment)
                attachment.add_header(
                    "content-disposition",
                    "attachment; filename = {}".format(fileName)
                )
                mail.attach(attachment)
        
        #convert message to string
        message = mail.as_string()
        mailServer="smtp.gmail.com"
        serverPortNum = 465

        #sending the email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(mailServer,serverPortNum,context=context) as serverConn:
            serverConn.login(self.senderEmail,password)
            serverConn.sendmail(
                self.senderEmail, self.receiverEmail, message
            )

    
if __name__ == "__main__":

    #without HTML
    """ 
    mail = Mail(senderEmail="smartCamSender2019@gmail.com", password="verysecurepassword")
    mail.addReceiver("RECEIVEREMAIL@gmail.com")
    mail.addSubjectHeader("TestSubjectHeader1")
    mail.addBody("TestBody1")
    mail.constructNSendMail()
    """

    #with HTML
    """
    mail = Mail(senderEmail="SENDEREMAIL@gmail.com", password="passwordHERE")
    mail.addReceiver("RECEIVEREMAIL@gmail.com")
    mail.addSubjectHeader("TestSubjectHeader2 WITH HTML")
    mail.addBody(
        "WithHTML", 
        html_context={
            'time_stamp': 'timestamp',
            'distance': 'distance',
    })
    mail.constructNSendMail()
    """

    #with attach file
    mail = Mail(senderEmail="smartCamSender2019@gmail.com", password="verysecurepassword")
    mail.addReceiver("smartCamReceiver2019@gmail.com")
    mail.addSubjectHeader("TestSubjectHeader3 WITH HTML")
    mail.addBody(
        "WithHTML", 
        html_context={
            'time_stamp': 'timestamp',
            'distance': 'distance',
    })
    mail.addAttachment(fileName="tux.jpg")
    mail.addAttachment(fileName="tux2.jpeg")
    mail.constructNSendMail()

    #terminal version
    #not terminal version doesn't have HTML support atm
    """
    mail = Mail(senderEmail="SENDEREMAIL@gmail.com")
    mail.constructNSendMail()
    """