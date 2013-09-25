# smartstart.py

A hacky proof of concept in Python showing lax security in DEI brand (Viper, Clifford, Python, etc) SmartStart remote start systems' iOS app (and possibly others).

All API requests are made via HTTPS, but the app doesn't validate certificates. This allows traffic to be easily spoofed with an HTTPS proxy. Username and password are sent in the GET requests from mobile devices over wifi or cellular data. Additionally, no noops are present and session IDs are also sent via parameter, so session hijacking and packet replay attacks may also be possible even if the username and password was not able to be sniffed.

**DISCLAIMER**: Each account has a fixed amount of API calls. My 3 year plan had 22500. You should be fine as long as you don't do anything stupid. This project does not sniff traffic, it's simply a demonstration of the app's API to show what is possible with the obtained data.

## Usage

### Setup

Assuming Python is installed, this script can be installed as follows:

    git clone git://github.com/nearengine/smartstart.py.git && cd smartstart.py
    mv _login.json login.json
    chmod +x smartstart.py
    
Then add your SmartStart credentials to `login.json` and:

    ./smartstart.py <command> [<device>]

You can omit the arguments for a list of commands. Windows users, you're on your own ;)

### Commands

    arm    - locks and arms the vehicle
    disarm - unlocks and disarms the vehicle
    trunk  - opens the trunk, if equipped
    panic  - starts the alarm
    remote - starts the engine
    locate - attempts to locate vehicle
    

An integer of range `0 - ?` is used for the optional second argument if you have multiple devices on your account.
