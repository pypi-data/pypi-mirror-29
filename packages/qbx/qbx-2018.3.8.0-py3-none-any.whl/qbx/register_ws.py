import json
import socket

import requests
from docopt import docopt as docoptinit

register_kong_doc = """
Usage:
    register_ws [options]
    
Options:
    --name=<name>
    --uri=<uri>
    --ip=<ip>
    --port=<port>
"""


def register_ws(argv):
    docopt = docoptinit(register_kong_doc, argv)
    r = requests.get('http://api.qbtrade.org/redis/get?key=config:wsv2&raw=1')
    r = r.json()
    port = docopt['--port']
    if not docopt['--ip']:
        ip = socket.gethostbyname(socket.gethostname())
    else:
        ip = docopt['--ip']
    uri = docopt['--uri']
    r[docopt['--name']] = f'ws://{ip}:{port}/{uri}'
    print(r)

    data = {'key': 'config:wsv2', 'value': json.dumps(r)}
    r = requests.post('http://api.qbtrade.org/redis/set', data)
    print(r.json())
    # r = requests.post(url, data=data)
    # print(docopt)
    # name = docopt['--name']
    # uris = docopt['--uris']
    # port = docopt['--port']
    # hosts = docopt['--hosts']
    # region = docopt['--region']
    # preserve = docopt['--preserve-host']
    # if region == 'alihz':
    #     url = 'http://alihz-master.qbtrade.org:8001/apis'
    # else:
    #     url = 'http://kong-admin.qbtrade.org/apis'
    # print('delete', r.text)
    # data = {'name': name,
    #         'upstream_url': 'http://{}:{}'.format(ip, port),
    #         }
    #
    # if hosts:
    #     data['hosts'] = hosts
    # if uris:
    #     data['uris'] = uris
    #     data['strip_uri'] = 'true'
    # if preserve:
    #     data['preserve_host'] = 'true'
    #
    # print(data)
    # r = requests.post(url, data=data)
    # print('add', r.text)
    # print('register ip', ip)


if __name__ == '__main__':
    # register_kong(['--name', 'pytest', '--ip', '1.2.3.4', '--uris', '/pytest', '--port', '8080'])
    register_ws(['--name', '/pytest', '--uri', '/ws', '--port', '3000'])
