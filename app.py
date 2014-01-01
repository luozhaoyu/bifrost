# -*- coding: utf-8 -*-
"""
    app.py
    ~~~~~~~~~~~~~~

    A brief description goes here.
"""
from bottle import run, route


@route('/index')
def index():
    return "hello, this is index"

def _main(argv):
    port = int(argv[1]) if len(argv) > 1 else 8080
    run(host='localhost', port=port)


if __name__ == '__main__':
    import sys
    _main(sys.argv)
