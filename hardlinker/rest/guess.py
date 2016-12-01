from hardlinker.linker import LinkInfo, FileInfo
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


class GuessAllResource(object):
    """
    :type guesser: Guesser
    """

    def __init__(self, guesser):
        self.guesser = guesser

    def on_get(self, req, resp):
        self.on_post(req, resp)

    def on_post(self, req, resp):
        result = self.guesser.guess_all()

        resp.json = [self._create_link_info_response(l) for l in result]

    def _create_link_info_response(self, link):
        """
        :type link: LinkInfo
        """
        result = self._create_file_info_response(link)
        result['links'] = [self._create_file_info_response(l) for l in link.links]

        return result

    def _create_file_info_response(self, info):
        """
        :type link: FileInfo
        """
        return {
            'folder': info.folder.name,
            'path': info.path,
            'name': info.name
        }
