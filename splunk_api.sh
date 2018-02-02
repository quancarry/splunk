#bin/bash

#Hostname Portal
host=localhost

#Authentication
admin=""
pass=""

#Content
title_m="$3"
body_m="$4"

#Sending request
curl -k -u $admin:$pass https://$host:8089/services/messages \
	-d name=$title_m \
	-d value="$body_m"
