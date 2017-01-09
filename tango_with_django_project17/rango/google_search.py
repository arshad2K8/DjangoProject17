__author__ = 'arshad'
import json
import urllib, urllib2, pprint
from googleapiclient.discovery import build

GOOGLE_API_KEY = 'AIzaSyA8IMsMe4EFl3mx5mAdHrhnWCQ_QWQ--8A'
googlurl = 'https://www.googleapis.com/customsearch/v1?parameters'
key=GOOGLE_API_KEY
CX = '016585465265343173652:e1cwh2kay9i'
#GET https://www.googleapis.com/customsearch/v1?key=INSERT_YOUR_API_KEY&cx=017576662512468239146:omuauf_lfve&q=lectures
'''
service = build("customsearch", "v1", developerKey=key)
res = service.cse().list(q='python',cx=CX).execute()

pprint.pprint(res)
pprint.pprint(res.keys())

pprint.pprint(res.get('url'))

items = res.get('items')
if items:
    for item in items:
        print 'Url of item is ', item.get('formattedUrl')
'''
def getSearchUrls(keywords):
    results = []
    try:
        listUrls = []
        service = build("customsearch", "v1", developerKey=key)
        res = service.cse().list(q=keywords,cx=CX).execute()
        items = res.get('items')
        for item in items:
            results.append({'title':item.get('title'), 'url':item.get('link'), 'summary':item.get('snippet')})
    except:
        print 'error during google search'

    return results

if __name__ == "__main__":
    print getSearchUrls('python')