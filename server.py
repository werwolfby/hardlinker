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
from hardlinker.linker import Linker, FolderInfo
from hardlinker.rest import create_api, AuthMiddleware
from hardlinker.rest.static_file import StaticFiles
from hardlinker.rest.links import LinkerResource
from hardlinker.rest.settings import SettingsResource, InputFoldersResource, OutputFoldersResource
from hardlinker.rest.guess import GuessItResource


def add_static_route(api, files_dir):
    file_dir = os.path.dirname(os.path.realpath(__file__))
    static_dir = os.path.join(file_dir, files_dir)
    api.add_route('/', StaticFiles(static_dir, 'index.html', False))
    api.add_route('/browse', StaticFiles(static_dir, 'index.html', False))
    for d, dirnames, files in os.walk(static_dir):
        parts = d[len(file_dir)+1:].split(os.path.sep)
        url = '/' + '/'.join(parts[1:] + ['{filename}'])
        api.add_route(url, StaticFiles(d, redirect_to_login=False))


def create_app(secret_key, token, linker):
    AuthMiddleware.init(secret_key, token, lambda: False)
    app = create_api()
    add_static_route(app, 'webapp')
    app.add_route('/api/links', LinkerResource(linker))
    app.add_route('/api/guessit', GuessItResource(linker))
    app.add_route('/api/settings', SettingsResource())
    app.add_route('/api/settings/input-folders', InputFoldersResource(linker))
    app.add_route('/api/settings/output-folders', OutputFoldersResource(linker))
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
        downloads = None
        shows = None
        movies = None

        def __init__(self, parser):
            parsed_args = parser.parse_args()

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

            env_debug = (os.environ.get('HARDLINKER_DEBUG', None) in ['true', 'True', '1'])

            self.debug = parsed_args.debug or env_debug or self.debug
            self.ip = parsed_args.ip or os.environ.get('HARDLINKER_IP', None) or self.ip
            self.port = parsed_args.port or try_int(os.environ.get('HARDLINKER_PORT', None)) or self.port
            self.downloads = parsed_args.downloads or os.environ.get('HARDLINKER_DOWNLOADS', None)
            self.shows = parsed_args.shows or os.environ.get('HARDLINKER_SHOWS', None)
            self.movies = parsed_args.movies or os.environ.get('HARDLINKER_MOVIES', None)

            has_output_folders = self.shows is not None or self.movies is not None

            if self.downloads is None:
                parser.error('downloads is not specified')

            if self.shows is None and self.movies is None:
                parser.error('shows or movies has to be specified')

    parser = argparse.ArgumentParser(description='Hardlinker server')
    parser.add_argument('--debug', action='store_true',
                        help='Run in debug mode. Secret key is always the same.')
    parser.add_argument('--ip', type=str, dest='ip',
                        help='Bind interface. Default is {0}'.format(Config.ip))
    parser.add_argument('--port', type=int, dest='port',
                        help='Port for server. Default is {0}'.format(Config.port))
    parser.add_argument('--config', type=str, dest='config',
                        default=os.environ.get('HARDLINKER_CONFIG', None),
                        help='Path to config file (default {0})'.format(Config.config))
    parser.add_argument('--downloads', type=str, dest='downloads',
                        help='Path to Downloads folder')
    parser.add_argument('--shows', type=str, dest='shows',
                        help='Path to Shows folder')
    parser.add_argument('--movies', type=str, dest='movies',
                        help='Path to Movies folder')

    config = Config(parser)

    debug = config.debug

    if debug:
        secret_key = 'Secret!'
        token = 'hardlinker'
    else:
        secret_key = os.urandom(24)
        token = ''.join(random.choice(string.ascii_letters) for _ in range(8))

    input_folders = [
        FolderInfo.from_path("Downloads", config.downloads)
    ]

    output_folders = []
    if config.shows is not None:
        output_folders.append(FolderInfo.from_path('Shows', config.shows))
    if config.movies is not None:
        output_folders.append(FolderInfo.from_path('Movies', config.movies))

    linker = Linker(input_folders, output_folders, ['mp4', 'avi', 'mkv'])

    app = create_app(secret_key, token, linker)
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
