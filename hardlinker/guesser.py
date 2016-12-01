from guessit import guessit
from hardlinker.linker import Linker, FileInfo, ShowsFolderInfo, MoviesFolderInfo


class Guesser(object):
    """
    :type linker: Linker
    """

    def __init__(self, linker):
        self.linker = linker

        shows_folders = filter(lambda f: isinstance(f, ShowsFolderInfo), self.linker.output_folders.values())
        movies_folders = filter(lambda f: isinstance(f, MoviesFolderInfo), self.linker.output_folders.values())

        self.shows_folder = shows_folders[0] if len(shows_folders) > 0 else None
        self.movies_folder = movies_folders[0] if len(movies_folders) > 0 else None

    def guess(self, folder, name):
        result = self._guess_name(name)

        return result

    def _guess_name(self, name):
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

        return FileInfo(folder, path, name)
