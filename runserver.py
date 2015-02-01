# -*- coding: utf-8 -*-
#!/usr/bin/env python
import argparse
from tuesday import app
from views import *


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', help='host of server')
    parser.add_argument('--port', help='port of server', type=int)
    args = parser.parse_args()
    options = {}
    if args.host:
        options['host'] = args.host
    if args.port:
        options['port'] = args.port
    app.run(**options)
