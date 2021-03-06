#!/usr/bin/python -u

import urllib
import httplib2
from xml.dom import minidom
import re
import time
from pprint import pprint
import sys
# Define Authentication & hostname.
baseurl = 'https://localhost:8089'
userName = 'admin'
password = 'anhquan1'
messages_title =sys.argv[1] #'Messses (%d) from script.' % count
messages_body = sys.argv[2] #'IP client '+m.group(1) + ' has overcome 10 requests all time . Totally has sent '+m.group(2) + ' requests.'


# Authenticate with server.
# Disable SSL cert validation. Splunk certs are self-signed.
serverContent = httplib2.Http(disable_ssl_certificate_validation=True).request(baseurl + '/services/auth/login',
    'POST', headers={}, body=urllib.urlencode({'username':userName, 'password':password}))[1]

sessionKey = minidom.parseString(serverContent).getElementsByTagName('sessionKey')[0].childNodes[0].nodeValue

# Set the service wants to interact with Splunk.

#List of services :
#Search : /services/search/jobs
#Message : /services/messages
#...
service_statement='/services/search/jobs/'
service='/services/messages'



payload = 'name': messages_title, 'value': messages_body}
        
#main function produce .
if len(sys.argv) < 3:
    httplib2.Http(disable_ssl_certificate_validation=True).request(baseurl + service, 'POST',
                                                                       headers={
                                                                           'Authorization': 'Splunk %s' % sessionKey},
                                                                       body=urllib.urlencode(payload))[1]
else:
    print 'Missing Argruments .'
    print 'python splunk_api.py <title> <content> .'
