#!/usr/bin/python -u

import urllib
import httplib2
from xml.dom import minidom
import re
import time
from pprint import pprint
# Define Authentication & hostname.
baseurl = 'https://localhost:8089'
userName = 'admin'
password = 'anhquan1'


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

flag=0

#Set the body of header request.
search_query='host="Centos web" | stats count by clientip'

payload_statement={'search': 'search '+search_query}

result=httplib2.Http(disable_ssl_certificate_validation=True).request(baseurl +service_statement,'POST',
    headers={'Authorization': 'Splunk %s' % sessionKey},body=urllib.urlencode(payload_statement))[1]
print baseurl +service_statement
regex=re.search(pattern='<sid>([\S]+)<\/sid>',string=result)

ID_search = regex.group(1)

# Echo the ID_search current.
print 'ID of jobs search current : ' + ID_search

urli=baseurl + service_statement + ID_search + '/results_preview'#_preview'
print urli

t=True
count=0
while(t):
    result_pre = httplib2.Http(disable_ssl_certificate_validation=True).request(urli, 'GET',
            headers={'Authorization': 'Splunk %s' % sessionKey})[1]

    if(re.match(pattern='^\<[\w]+ [\w]+\=\'[1]\'\/\>$',string=result_pre)):
        print 'ID of jobs search current : ' + ID_search
        time.sleep(10)
        count+=1
        t=True
        if count > 100:
            t=False
        else:
            print 'Waiting for process ' + str(count)+'0 s.'
    else:
        t=False
re2=re.finditer (pattern="<field k='clientip'>(?:[\s]*?)<value><text>([\S]+)<\/text><\/value>(?:[\s]*?)<\/field>(?:[\s]*?)<field k='count'>(?:[\s]*?)<value><text>([\S]+)<\/text><\/value>(?:[\s]*?)<\/field>",string=result_pre)

count=0
for m in re2:

    if (int(m.group(2))>10):
        # Perform request.
        # Again, disable SSL cert validation.

        # Create Title and body of messages.
        count=count+1
        messages_title = 'Messses (%d) from script.' % count
        messages_body = 'IP client '+m.group(1) + ' has overcome 10 requests all time . Totally has sent '+m.group(2) + ' requests.'

        payload = {'name': messages_title, 'value': messages_body}

        httplib2.Http(disable_ssl_certificate_validation=True).request(baseurl + service, 'POST',
                                                                       headers={
                                                                           'Authorization': 'Splunk %s' % sessionKey},
                                                                       body=urllib.urlencode(payload))[1]
