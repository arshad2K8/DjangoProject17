__author__ = 'arshad'
import smtplib
from django.core.mail import send_mail

def send_email(fromadd='from@gmail.com', toadd='send@gmail.com'):

    msg='''hi,how r u'''
    username='abc@gmail.com'
    passwd='password'

    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(username,passwd)

        server.sendmail(fromadd,toadd,msg)
        print("Mail Send Successfully")
        server.quit()

    except:
        print("Error:unable to send mail")


def djangoSendEmail():
    send_mail(
    'Subject here',
    'Here is the message.',
    'from@example.com',
    ['to@example.com'],
    fail_silently=False,)
