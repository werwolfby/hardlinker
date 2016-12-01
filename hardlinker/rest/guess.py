from guessit import guessit
from hardlinker.linker import Linker, ShowsFolderInfo, MoviesFolderInfo


class GuessItResource(object):
    """
    :type shows_folder: ShowsFolderInfo
    :type movies_folder: MoviesFolderInfo
    """

    def __init__(self, linker):
        """
        :type linker: Linker
        """
        self.linker = linker
        shows_folders = filter(lambda f: isinstance(f, ShowsFolderInfo), self.linker.output_folders.values())
        movies_folders = filter(lambda f: isinstance(f, MoviesFolderInfo), self.linker.output_folders.values())

        self.shows_folder = shows_folders[0] if len(shows_folders) > 0 else None
        self.movies_folder = movies_folders[0] if len(movies_folders) > 0 else None

    def on_get(self, req, resp):
        folder = req.get_param('folder', required=True)
        file_path = req.get_param('path', required=True)

        path = file_path.split('/')

        name = path[-1]
        guess = guessit(name)

        if guess['type'] == 'episode':
            folder = self.shows_folder
            show = guess['title']
            season = guess['season']

            folder.read_shows()
            (show, season) = folder.find_show(show, season)

            path = [show, season]
        else:
            folder = self.movies_folder
            path = []

        resp.json = {
            'folder': folder.name,
            'path': path,
            'name': name
        }
