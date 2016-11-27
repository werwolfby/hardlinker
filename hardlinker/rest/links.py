from hardlinker.linker import Linker, FileInfo, LinkInfo, FolderInfo


class LinkerResource(object):
    def __init__(self, linker):
        """
        :type linker: Linker
        """
        self.linker = linker

    def on_get(self, req, resp):
        links = self.linker.links

        resp.json = [self._create_link_response(l) for l in links]

    @staticmethod
    def _create_link_response(link):
        """
        :type link: LinkInfo
        """
        resp = LinkerResource._create_file_info_response(link)

        resp['links'] = [LinkerResource._create_file_info_response(l) for l in (link.links or [])]

        return resp

    @staticmethod
    def _create_file_info_response(info):
        """
        :type info: FileInfo
        """
        return {
            'folder': info.folder.name,
            'path': info.path or [],
            'name': info.name
        }

