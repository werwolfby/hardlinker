import os
from guessit import guessit


class GuessItResource(object):
    def on_get(self, req, resp):
        folder = req.get_param('folder', required=True)
        file_path = req.get_param('filepath', required=True)

        path = file_path.split('/')

        resp.json = guessit(path[-1])
