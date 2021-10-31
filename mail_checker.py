###-Sets account's password and adress-###
addr = "Your email here"
passwrd = "Your password here"

#################################################################
#################################################################
##                                                             ##
##                CHECKS FOR NEW MAILS                         ##
##                                                             ##
#################################################################
#################################################################

import binascii
import platform
import imaplib
import os
import requests
import subprocess
import email
import email.header
from datetime import datetime, timedelta
from base64 import b64decode
import quopri
########################-Functions-########################


###-Check if the user is connected to internet-###
def internetTest():
    url = "https://www.google.com"
    timeout = 5
    try:
        request = requests.get(url, timeout=timeout)
        return True
    except (requests.ConnectionError, requests.Timeout) as exception:
        return False


def addToBody(content, separator, charset):
    global body
    content = str(content, charset, "ignore")
    if content == '':
        content = '\n'
    elif content == '>':
        content = '\n>\n' 
    bodytxt.append(content)
    body = separator.join(bodytxt)

########################-actual code-########################
a = False
###-loop while the user is not connected to the internet-###
while not(a):
    a = internetTest()


###-Sets up server to get the mails-###
server = imaplib.IMAP4_SSL('imap.gmail.com', '993')
try:
    server.login(addr, passwrd)
except imaplib.IMAP4.error as error:
    print("An error occured: wrong ceditentials\n\nCheck your email and password and make sure that you have enabled the less secure apps acess on your gmail account.\nFor more informations about less secure apps, go to https://support.google.com/a/answer/6260879")
    input("Press return to leave")
    exit()
server.select('Inbox')

###-Gets the amount of unseen mails-###
unFilteredstr = str(server.status("INBOX", "(UNSEEN)")[1][0])
unFilteredstr = unFilteredstr.replace("""b'"INBOX" (UNSEEN """, "")
filteredStr = unFilteredstr.replace(""")'""", "")
unseenAmount = int(filteredStr)

###-Gets unssen messages index for the last 7 days-###
n_days_ago = datetime.now() - timedelta(days=7)
n_days_ago_str = "{0}".format(n_days_ago.strftime("%d-%b-%Y"))
satus, data = server.search(None, "(SINCE "+ n_days_ago_str+ ")", "Unseen")




###-Create the text file-###
path = os.getcwd() + "\\" + "unseen.txt"
f = open(path, "w+")

message2 = "\nUnseen mails for the last 7 days"
###-Sets the message accordingly to the amount of messages-###
if unseenAmount == 0:
    message = "0 new mails"
    message2 = ""
elif unseenAmount == 1:
    message = "1 new mail"
else:
    message = str(unseenAmount) + " new mails"

message += " on " + addr + " since the " + n_days_ago_str
f.write(message)
f.write(message2)


for num in data[0].split():
    fromAddr = ""
    toAddr = ""
    subject = ""
    date = ""
    body = ""
    bodytxt = []
    ##############-Getting the header of the mail-##############
    status, data = server.fetch(num, '(BODY[HEADER.FIELDS (SUBJECT DATE FROM TO )])')               #####GET THE BODYYYYYYY
    email_msg = data[0][1]                                          #
    mail_str = str(email_msg)                                       #
    mail_str = mail_str.replace("b'", "")                           #
    textList = mail_str.split("\\r\\n")                             #Cleans up the string
    for i in textList:
        if "From" in i:
            fromAddr = i.replace("From: ", "")
        elif "Date" in i:
            date = i
        elif "To" in i:
            toAddr = i
        elif "Subject" in i:
            if "=?utf-8" in i.lower() or "iso-8859-1" in i:
                subjectTuple = email.header.decode_header(i)
                subject = str(subjectTuple[1][0], subjectTuple[1][1])
            else:
                subject = i.replace("Subject:", "")

    ##############-Getting the body of the mail-##############
    ###-Getting raw string and body-###
    status, data = server.fetch(num, "(RFC822)")
    raw_email_string = data
    ###-get the message and payload from the raw string (it's still pretty raw, but more readable)-###
    email_message = email.message_from_string(str(data))
    raw_txt = email_message.get_payload()
    ###-Gets straight to the part that interests us, aka after 'Content-type'-###
    raw_txt = raw_txt.split("Content-Type")
    for part in raw_txt:
        if "text/plain" in part:
            ###-When it finds the plain text part(the part that interests us), it starts extracting infos and splitting the string-###
            part = part.replace(': text/plain; charset="', "")              #Clears the beggining of the string
            encoding = part.split('Content-Transfer-Encoding: ')            #
            encoding = encoding[1].split("\\r")[0]                          #Gets the mail encoding 
            charset = part.split('"')[0]                                    #Gets the charset of the mail (aka how the characters are encoded to the browser)
            sorting = part.split("\\r\\n")                                  #
            sorting = sorting[3:]                                           #
            del sorting[-1]                                                 #
            del sorting[-1]                                                 #Sorts the list to get the stuff that interests us
            for i in sorting:
                if encoding == "base64":
                    try:
                        i = b64decode(i)
                    except binascii.Error as error:
                        print("Error decoding base64 string")
                elif encoding == "quoted-printable":                         #Decode the string according to their encoding:
                    i = quopri.decodestring(i)                              #

                if charset.lower() == "utf-8":                              #
                    addToBody(i, "", charset)                               #
                elif charset.lower() == "iso-8859-1":                       #Same but for the charset
                    addToBody(i, "\n", charset)                             #
                elif charset.lower() == "us-ascii":
                    bodytxt.append(i)
                    body = "\n".join(bodytxt)
    f.write("\n\n\n#########################-New email from " + fromAddr + "-#########################")
    f.write("\n" + date)
    try:
        f.write("\Subject: " + subject)
    except UnicodeEncodeError as error:
        f.write("\nError: Cloud not get the subject")
    try:    
        if body == "":
            raise Exception("Could not get the body or empty body")
        f.write("\nBody:\n" + body)
    except (UnicodeEncodeError, Exception) as error:
        f.write("\nError: Could not get the body")
f.close()


###-leave server-###
server.close()


###-Opening the file using the system's file reader-###
userSystem = platform.system().lower()

if userSystem == "windows":
    subprocess.call(['C:\\Windows\\System32\\notepad.exe', path])
elif userSystem == "linux" or userSystem =="Darwin":
    subprocess.call(['nano', path])
else:
    print("Unknown os")



###-Removes the text file-###
os.remove(path)
