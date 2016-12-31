__author__ = 'arshad'
import json
import urllib, urllib2
from googleapiclient.discovery import build
GOOGLE_API_KEY = 'AIzaSyA8IMsMe4EFl3mx5mAdHrhnWCQ_QWQ--8A'
googlurl = 'https://www.googleapis.com/customsearch/v1?parameters'
key=GOOGLE_API_KEY
CX = '016585465265343173652:e1cwh2kay9i'
#GET https://www.googleapis.com/customsearch/v1?key=INSERT_YOUR_API_KEY&cx=017576662512468239146:omuauf_lfve&q=lectures

service = build("customsearch", "v1", developerKey=key)
res = service.cse().list(q='lectures',cx=CX).execute()