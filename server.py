#!/usr/bin/env python
from builtins import range
import os
import sys
import six
import random
import string
import argparse
import warnings
from cherrypy import wsgiserver
from hardlinker.rest import create_api, AuthMiddleware
from hardlinker.rest.static_file import StaticFiles


def add_static_route(api, files_dir):
    file_dir = os.path.dirname(os.path.realpath(__file__))
    static_dir = os.path.join(file_dir, files_dir)
    api.add_route('/', StaticFiles(static_dir, 'index.html', False))
    api.add_route('/browse', StaticFiles(static_dir, 'index.html', False))
    #api.add_route('/styles/monitorrent.css', StaticFiles(os.path.join(static_dir, 'styles'), 'monitorrent.css', False))
    for d, dirnames, files in os.walk(static_dir):
        parts = d[len(file_dir)+1:].split(os.path.sep)
        url = '/' + '/'.join(parts[1:] + ['{filename}'])
        api.add_route(url, StaticFiles(d, redirect_to_login=False))


def create_app(secret_key, token):
    AuthMiddleware.init(secret_key, token, None)
    app = create_api()
    add_static_route(app, 'webapp')
    return app


def main():
    def try_int(s, base=10, val=None):
        if s is None:
            return None
        try:
            return int(s, base)
        except ValueError:
            return val

    class Config(object):
        debug = False
        ip = '0.0.0.0'
        port = 4735                      # HRDL on phone keyboard
        config = 'config.py'

        def __init__(self, parsed_args):
            if parsed_args.config is not None and not os.path.isfile(parsed_args.config):
                warnings.warn('File not found: {}'.format(parsed_args.config))
            config_path = parsed_args.config or self.config
            if os.path.isfile(config_path):
                # noinspection PyBroadException
                try:
                    parsed_config = {}
                    with open(config_path) as config_file:
                        six.exec_(compile(config_file.read(), config_path, 'exec'), {}, parsed_config)
                    self.debug = parsed_config.get('debug', self.debug)
                    self.ip = parsed_config.get('ip', self.ip)
                    self.port = parsed_config.get('port', self.port)
                    self.db_path = parsed_config.get('db_path', self.db_path)
                except:
                    ex, val, tb = sys.exc_info()
                    warnings.warn('Error reading: {0}: {1} ({2}'.format(parsed_args.config, ex, val))

            env_debug = (os.environ.get('MONITORRENT_DEBUG', None) in ['true', 'True', '1'])

            self.debug = parsed_args.debug or env_debug or self.debug
            self.ip = parsed_args.ip or os.environ.get('MONITORRENT_IP', None) or self.ip
            self.port = parsed_args.port or try_int(os.environ.get('MONITORRENT_PORT', None)) or self.port

    parser = argparse.ArgumentParser(description='Hardlinker server')
    parser.add_argument('--debug', action='store_true',
                        help='Run in debug mode. Secret key is always the same.')
    parser.add_argument('--ip', type=str, dest='ip',
                        help='Bind interface. Default is {0}'.format(Config.ip))
    parser.add_argument('--port', type=int, dest='port',
                        help='Port for server. Default is {0}'.format(Config.port))
    parser.add_argument('--config', type=str, dest='config',
                        default=os.environ.get('MONITORRENT_CONFIG', None),
                        help='Path to config file (default {0})'.format(Config.config))

    parsed_args = parser.parse_args()
    config = Config(parsed_args)

    debug = config.debug

    if debug:
        secret_key = 'Secret!'
        token = 'monitorrent'
    else:
        secret_key = os.urandom(24)
        token = ''.join(random.choice(string.ascii_letters) for _ in range(8))

    app = create_app(secret_key, token)
    d = wsgiserver.WSGIPathInfoDispatcher({'/': app})
    server_start_params = (config.ip, config.port)
    server = wsgiserver.CherryPyWSGIServer(server_start_params, d)
    print('Server started on {0}:{1}'.format(*server_start_params))

    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()


if __name__ == '__main__':
    main()
