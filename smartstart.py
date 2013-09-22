#!/usr/bin/env python

import time, sys, json, os
import requests

man = '''
Usage:
smartstart.py <command> [<device>]

Commands:
arm    - locks and arms the vehicle
disarm - unlocks and disarms the vehicle
trunk  - opens the trunk, if equipped
panic  - starts the alarm
remote - starts the engine
locate - attempts to locate vehicle

Devices:
An integer of range 0-? (use if you have multiple devices on your account)
'''

# API parameters
url_base = 'https://colt.calamp-ts.com/'
commands = ['arm', 'disarm', 'panic', 'trunk', 'remote', 'locate']

# Check for at least one command line argument, otherwise print the help screen
if len(sys.argv) < 2:
    print man
    sys.exit()

# Make sure <command> is present in the list of available API endpoints above,
# otherwise print the help screen
if sys.argv[1] in commands:
    command = sys.argv[1]
else:
    print man
    sys.exit()

# This checks if a <device> is present in the arguments. If it's a number,
# it uses it as the device selector, in case if you have multiple devices on
# your account. Otherwise, it defaults to 0
try:
    sys.argv[2]
except:
    dev_sel = 0
else:
    if sys.argv[2].isdigit():
        dev_sel = sys.argv[2]
    else:
        dev_sel = 0

# Load username & password from config file as JSON
fpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'login.json')
try:
    user = open(fpath)
    user = json.load(user)
except:
    print 'error parsing login.json'
    sys.exit()

# Get a session ID
s = requests.session()
r = s.get(url_base + 'auth/login/' + user["username"] + '/' + user["password"])

try:
    sess_res = json.loads(r.text)
    sess_id = sess_res["Return"]["Results"]["SessionID"]
    print 'login success! sessid: ' + sess_id
except:
    print 'error getting session ID, incorrect user/pass?'
    sys.exit()

# Get list of vehicles
r = s.get(url_base
    + 'device/advancedsearch/null/100/0/ActiveWithAsset/null/false?sessid='
    + sess_id)

try:
    device_info = json.loads(r.text)
    device_id = device_info["Return"]["Results"]["Devices"][dev_sel]["DeviceId"]
except:
    print 'error getting device ID'
    sys.exit()

# Carry out command
r = s.get(url_base
    + 'device/sendcommand/'
    + device_id
    + '/'
    + command
    + '?sessid='
    + sess_id)

try:
    res = json.loads(r.text)
    print 'response returned: '
    print json.dumps(res, indent=4)
except:
    print 'error parsing response json'
    sys.exit()
