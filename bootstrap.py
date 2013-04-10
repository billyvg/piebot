from db import db

if db.configuration.find().count() == 0:
    data = [{'key': 'network',
            'value': 'localhost',
            'description': 'The name of the network to connect to. (temp. )'},
            {'key': 'port',
            'value': '6667',
            'description': 'The port of the IRC server.'},
            {'key': 'nickname',
            'value': 'ppbot',
            'description': 'The nickname that the bot should use.'},
            {'key': 'password',
            'value': '',
            'description': 'The password for a server if necessary'},
            {'key': 'alt_nickname',
            'value': 'ppbot_',
            'description': 'An alternate nickname the bot should use if the primary is in use.'},
            {'key': 'realname',
            'value': 'Powered by billy',
            'description': 'The "real name" field displayed on /whois.'},
            {'key': 'me',
            'value': 'billy',
            'description': 'lol...'},
            {'key': 'trigger',
            'value': '.',
            'description': 'The trigger that the bot should respond to.'}
            ]
    db.configuration.insert(data)


if db.access_levels.find().count() == 0:
    data = [{'level': 0,
            'name': 'owner'},
            {'level': 1,
            'name': 'master'},
            {'level': 2,
            'name': 'op'},
            {'level': 3,
            'name': 'user'},
            {'level': 4,
            'name': 'guest'},
            {'level': 5,
            'name': 'all'}
            ]
    db.access_levels.insert(data)

if db.networks.find().count() == 0:
    data = [{'name': 'gamesurge'},
            {'name': 'freenode'}]
    db.networks.insert(data)

if db.servers.find().count() == 0:
    data = [{'network': 'gamesurge',
            'address': 'irc.gamesurge.net',
            'port': 6667,
            'nickname': 'ppbot',
            'alt_nickname': 'ppbot'},
            {'network': 'freenode',
            'address': 'irc.freenode.org',
            'port': 6667,
            'nickname': 'ppbot',
            'alt_nickname': 'ppbot'}]
    db.servers.insert(data)

if db.channels.find().count() == 0:
    data = [{'network': 'gamesurge',
            'name': '#channel'},
            {'network': 'freenode',
                'name': '##channel'}]


