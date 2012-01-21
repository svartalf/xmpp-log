# -*- coding: utf-8 -*-

import datetime
import psycopg2
import xmpp

import settings

# Cached database ids
conferences = {}

for conference in settings.CONFERENCES:
    conferences[conference] = None

connection = psycopg2.connect("dbname='%(name)s' host='%(host)s' user='%(user)s' password='%(password)s'" % settings.DATABASE)
cursor = connection.cursor()

def log(session, msg):
    if msg.getType() == 'groupchat':
        dt = msg.getTimestamp()
        if not dt:
            dt = msg.setTimestamp()
            dt = msg.getTimestamp()
        try:
            dt = datetime.datetime.strptime(dt, '%Y%m%dT%H:%M:%S')
            dt += datetime.timedelta(hours=8) # Irkutsk timezone
        except ValueError:
            dt = datetime.datetime.now()
        conf = msg.getFrom().getStripped()
        user = msg.getFrom().getResource()
        body = msg.getBody()

        if conf in conferences:
            conf_id = conferences[conf]
            cursor.execute('INSERT INTO logs(conference_id, date, "user", "text", "type") VALUES (%s, %s, %s, %s, %s);',
                (conf_id, dt, user, body, 4))

def ping(session, iq):
    global client
    for child in iq.getChildren():
        if child.name == 'ping' and iq.getType() == 'get':
            reply = iq.buildReply('result')
            session.send(reply)
            raise xmpp.NodeProcessed

if __name__ == '__main__':
    jid = xmpp.JID(settings.JID)
    client = xmpp.Client(jid.getDomain(), debug=[])
    client.connect()
    client.RegisterHandler('iq', ping)
    client.auth(jid.getNode(), settings.PASSWORD)
    client.sendInitPresence()

    for conf in conferences.keys():
        cursor.execute('SELECT id FROM conferences WHERE name = %s;', (conf,))
        data = cursor.fetchone()
        if not data:
            cursor.execute('INSERT INTO conferences("name") VALUES (%s) RETURNING id;', (conf,))
            connection.commit()
            data = cursor.fetchone()

        conferences[conf] = data[0]
        init = xmpp.Presence(to='%s/Yarrr' % conf)
        init.setTag('x', namespace=xmpp.NS_MUC)
        init.getTag('x').addChild('history', {'maxchars':'0', 'maxstanzas':'0'})
        client.send(init)

    try:
        while True:
            client.Process(10)
    except KeyboardInterrupt:
        presence = xmpp.Presence(typ='unavailable')
        client.send(presence)
        client.disconnect()
