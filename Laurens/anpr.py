#!/usr/bin/python

# pip install requests
import requests
import re
regions = ['be', 'nl'] # Change to your country
with open('/home/pi/IOTAdv/auto.jpg', 'rb') as fp:
    response = requests.post(
        'https://api.platerecognizer.com/v1/plate-reader/',
        data=dict(regions=regions),  # Optional
        files=dict(upload=fp),
        headers={'Authorization': 'Token 4c3b2d68309ebeccb621b762e2ecc6b09d72a7b5'})
plate = response.json()['results'][0]['plate']
# plate = "toyota"
if re.search(r'^[0-9][a-z]{3}[0-9]{3}$' , plate):
    print("{}-{}-{}".format(plate[0], plate[1:4], plate[4:]).upper())
elif re.search(r'^[a-z]{3}[0-9]{3}$|^[0-9]{3}[a-z]{3}$' , plate):
    print("{}-{}".format(plate[0:3], plate[3:]).upper())
else:
    print(plate.upper())

