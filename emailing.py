import smtplib
import mimetypes
from email.message import EmailMessage
import os

SENDER = 'cengsoftware.testing99@gmail.com'
PASSWORD = 'hmhp npio jwdn cuoe'

RECIPIENT = 'asusmfs2019@gmail.com'


def send_email(image_path):
    print("send_email function started")
    msg = EmailMessage()
    msg['From'] = SENDER
    msg['To'] = RECIPIENT

    msg['Subject'] = "New customer showed up!"
    msg.set_content("Hey, we just saw a new customer!")

    file_name = os.path.basename(image_path)

    mime_type, _ = mimetypes.guess_type(image_path)


    if mime_type:
        maintype, subtype = mime_type.split('/')
    else:
        maintype = 'application'
        subtype = 'octet-stream'


    with open(image_path, mode='rb') as file:
        content = file.read()

    msg.add_attachment(content,
                       maintype=maintype,
                       subtype=subtype,
                       filename=file_name)  # <-- Bu satır, dosya adını gönderir.


    try:
        gmail = smtplib.SMTP('smtp.gmail.com', 587)
        gmail.ehlo()
        gmail.starttls()
        gmail.login(SENDER, PASSWORD)
        gmail.sendmail(SENDER, RECIPIENT, msg.as_string())
        gmail.quit()
    except smtplib.SMTPException:
        print('Error: unable to send email')

    print("send_email function ended")


if __name__ == '__main__':
    send_email(image_path = "images/20.jpg")
    print('done')

