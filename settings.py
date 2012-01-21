# -*- coding: utf-8 -*-

# JID for connection
JID = ''
PASSWORD = ''

# MUC JID's
CONFERENCES = ()

# Database settings, obviously
DATABASE = {
    'host': '',
    'name': '',
    'user': '',
    'password': '',
}

try:
    from settings_local import *
except ImportError:
    import traceback, sys
    traceback.print_exc()
    sys.exit()