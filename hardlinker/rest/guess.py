from guessit import guessit
from hardlinker.linker import Linker


class GuessItResource(object):
    def __init__(self, linker):
        """
        :type linker: Linker
        """
        self.linker = linker
        shows_folders = filter(lambda f: f.name == "Shows", self.linker.output_folders.values())
        movies_folders = filter(lambda f: f.name == "Movies", self.linker.output_folders.values())

        self.shows_folder = shows_folders[0].name if len(shows_folders) > 0 else None
        self.movies_folder = movies_folders[0].name if len(movies_folders) > 0 else None

    def on_get(self, req, resp):
        folder = req.get_param('folder', required=True)
        file_path = req.get_param('filepath', required=True)

        path = file_path.split('/')

        name = path[-1]
        guess = guessit(name)

        if guess['type'] == 'episode':
            folder = self.shows_folder
            path = [guess['title'], 'Season {0}'.format(guess['season'])]
        else:
            folder = self.movies_folder
            path = []

        resp.json = {
            'folder': folder,
            'path': path,
            'name': name
        }
