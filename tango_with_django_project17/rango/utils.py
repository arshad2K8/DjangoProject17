__author__ = 'arshad'
import smtplib
from django.core.mail import send_mail
from googleapiclient.discovery import build
import pprint

def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res['items']

#results = google_search('stackoverflow site:en.wikipedia.org', my_api_key, my_cse_id, num=10)

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



import json
import urllib, urllib2

# Add your BING_API_KEY

BING_API_KEY = '<insert_bing_api_key>'

def run_query(search_terms):

    results = []
    results.append({
            'title': 'sample title',
            'link': 'sample url',
            'summary': 'sample description'})
    # Return the list of results to the calling function.
    return results


def get_deals_from_hof():
    ValidDeals = []
    ValidDeals.append({'title':'Book1', 'oldprice':20, 'newprice':30})
    return ValidDeals
