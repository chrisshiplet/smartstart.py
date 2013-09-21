#!/usr/bin/env python

import time, sys, json
import requests

s = requests.session()
r = s.get('https://colt.calamp-ts.com/auth/login/user/pass')

