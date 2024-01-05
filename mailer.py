#!/usr/bin/python

from sys import exit
from optparse import OptionParser
from optparse import Option, OptionValueError
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
import re
import base64
import configparser
import os

class Mail:
    def __init__(self):
        self.isHTML = False
        self.plainTextBody = None
        self.htmlMessageBody = None
        self.attachments = []
        self.configurationFile = ".mailerrc"

        """
        Format for self.configurationFile :
            [SMTP]
                host = send.one.com
                port = 587
                starttls = True
                login = <some_address>
                secret = <some_clear_text_secret>
                senderAddress = <some_address_perhaps_the_same_as_login>
        """

    def setConfigurationFile(self, fn):
        self.configurationFile = fn

    def attachFile(self, attachment):
        self.attachments.append(attachment)

    def setRecieverAddress(self, a):
        self.recieverAddress = a

    def setMessageSubject(self, s):
        self.messageSubject = s

    def setHTMLMessageBody(self, b):
        self.htmlMessageBody = b

    def setPlainTextMessageBody(self, b):
        self.plainTextBody = b

    def send(self):

        text = ""
        html = ""

        if self.plainTextBody and not self.htmlMessageBody :
            html = self.plainTextBody

        elif not self.plainTextBody and self.htmlMessageBody :
            text = re.sub('<[^<]+?>', '', self.htmlMessageBody)
            html = self.htmlMessageBody

        elif self.plainTextBody and self.htmlMessageBody :
            text = self.plainTextBody
            html = self.htmlMessageBody

        else:
            print("Nuffin")
            exit(1)

        text_part = MIMEText(text, 'plain')
        html_part = MIMEText(html, 'html')

        msg_alternative = MIMEMultipart('alternative')
        msg_alternative.attach(text_part)
        msg_alternative.attach(html_part)

        msg_mixed = MIMEMultipart('mixed')
        msg_mixed.attach(msg_alternative)




        for filename in self.attachments:
            try:
                visualName = os.path.basename(filename)
                subtype = os.path.splitext(visualName)[1].replace(".","")
                fp=open(filename,'rb')
                attachment = MIMEApplication(fp.read(),_subtype=subtype)
                fp.close()
                attachment.add_header('Content-Disposition', 'attachment', filename=visualName)
                msg_mixed.attach(attachment)
            except FileNotFoundError:
                print("Could not find file '"+filename+"' for attachment.")
                return False
            except PermissionError:
                print("Insufficient persmissions to read file '"+filename+"' for attachment")
                return False

        try:

            config_object = configparser.ConfigParser()
            with open(self.configurationFile,"r") as file_object:
                config_object.read_file(file_object)
                host = config_object.get("SMTP", "host")
                starttls = config_object.getboolean("SMTP", "starttls")
                port = config_object.getint("SMTP", "port")
                login = config_object.get("SMTP", "login")
                secret = config_object.get("SMTP", "secret")
                senderAddress = config_object.get("SMTP", "senderAddress")

        except FileNotFoundError:
            print("Could not open mail server configuration file '"+self.configurationFile+"' ")
            return False
        except PermissionError:
            print("Insufficient persmissions to read configuration file '"+self.configurationFile+"'")
            return False
        except ValueError as ve:
            print("Error parsing mail server configuration: "+str(ve))
            return False

        except configparser.NoSectionError as ke:
            print("Config file is corrupt or incomplete: "+str(ke)+"")
            return False

        msg_mixed['From'] = senderAddress
        msg_mixed['To'] = self.recieverAddress
        msg_mixed['Subject'] = self.messageSubject

        smtp = smtplib.SMTP(host, port=port)
        if starttls:
            smtp.starttls()

        smtp.login(login, secret)
        smtp.sendmail(msg_mixed['From'], msg_mixed['To'], msg_mixed.as_string())
        smtp.quit()

        return True



if __name__ == "__main__":

    parser = OptionParser(usage="%prog [options] <RECIEVER_ADDRESS> <MESSAGE_SUBJECT> <MESSAGE_HTML_BODY>")
    parser.add_option("-a", "--attach", action="append", dest="attachments", help="File to attach. May be specified multiple times.", default=[])
    parser.add_option("-S", "--subjectIsBase64", action="store_true", dest="subjectIsBase64", help="Subject of the mail is base64 encoded", default=False)
    parser.add_option("-B", "--bodyIsBase64", action="store_true", dest="messageBodyIsBase64", help="Message body of the mail is base64 encoded", default=False)
    parser.add_option("-r", "--recieverName", action="store", dest="recieverName", help="Name of the reciever to use. This is a real name and not che email address", default=None)
    parser.add_option("-p", "--plainTextMessage", action="store", dest="plainTextBody", help="An optional plain text body to use. If omitted, the plain text body of the mail will be the HTML body stripped for tags.", default=None)
    parser.add_option("-P", "--plainTextMessageIsBase64", action="store_true", dest="treatPlainTextBodyAsBase64", help="", default=False)
    parser.add_option("-c", "--configuration", action="store", dest="configurationFile", help="File in .ini format specifying details on the SMTP server to use.", default=".mailerrc")



    (options, args) = parser.parse_args()

    if len(args) < 3:
        print("Too few arguments. Run with -h to get help.")
        exit(1)

    if len(args) > 3:
        print("Too many arguments. Run with -h to get help.")
        exit(1)

    mail = Mail()

    mail.setConfigurationFile(options.configurationFile)

    for attachment in options.attachments:
        mail.attachFile(attachment)

    mail.setRecieverAddress(args[0])

    if options.subjectIsBase64:
        mail.setMessageSubject(base64.b64decode(args[1]).decode("utf-8"))
    else:
        mail.setMessageSubject(args[1])

    if options.messageBodyIsBase64:
        mail.setHTMLMessageBody(base64.b64decode(args[2]).decode("utf-8"))
    else:
        mail.setHTMLMessageBody(args[2])

    if options.plainTextBody:
        if options.treatPlainTextBodyAsBase64:
            mail.setPlainTextMessageBody(base64.b64decode(options.plainTextBody).decode("utf-8"))
        else:
            mail.setPlainTextMessageBody(options.plainTextBody)

    if not mail.send():
        exit(1)
    else:
        exit(0)
