from hardlinker.guesser import Guesser


class GuessItResource(object):
    """
    :type shows_folder: ShowsFolderInfo
    """

    def __init__(self, guesser):
        """
        :type guesser: Guesser
        """
        self.guesser = guesser

    def on_get(self, req, resp):
        folder = req.get_param('folder', required=True)
        file_path = req.get_param('path', required=True)

        path = file_path.split('/')

        name = path[-1]
        result = self.guesser.guess(folder, name)

        resp.json = {
            'folder': result.folder.name,
            'path': result.path,
            'name': result.name
        }
