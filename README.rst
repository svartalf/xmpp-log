Simple ``XMPP`` MUC logger.

Installation
===============

1. Create a virtual environment (preferable way, really!) with a `virtualenv`

    virtualenv .env

2. Install required libraries

    .env/bin/pip install -r .requirements.txt

3. Create file with a local settings

    touch settings_local.py

4. Copy this template and change it with your settings

    JID = 'logger-jid@example.org'
    PASSWORD = 'jid-password'

    CONFERENCES = (
        'lolcats@conference.example.org',
        'gifs@conference.example.org',
    )

    DATABASE = {
        'host': 'localhost',
        'name': 'database_name',
        'user': 'database_user',
        'password': 'database_password',
    }

5. Run it

    .env/bin/python main.py
