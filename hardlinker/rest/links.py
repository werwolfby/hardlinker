from hardlinker.linker import Linker, LinkInfo, FolderInfo


class FileInfoResponse(object):
    def __init__(self, folder, path, name):
        """
        :type folder: FolderInfo
        :type path: str
        :type name: str
        """
        self.folder = folder
        self.path = path
        self.name = name

    def to_dict(self):
        return {
            'folder': {
                'name': self.folder.name,
                'path': self.folder.path
            },
            'path': self.path,
            'name': self.name
        }


class LinkInfoResponse(FileInfoResponse):
    def __init__(self, folder, path, name, links):
        """
        :type links: list[FileInfoResponse]
        """
        super(LinkInfoResponse, self).__init__(folder, path, name)
        self.links = links

    def to_dict(self):
        base = super(LinkInfoResponse, self).to_dict()

        base['links'] = [l.to_dict() for l in self.links]

        return base


class LinkerResource(object):
    def __init__(self, linker):
        """
        :type linker: Linker
        """
        self.linker = linker

    def on_get(self, req, resp):
        links = self.linker.links

        resp.json = [self._create_link_response(l).to_dict() for l in links]

    def _create_link_response(self, link):
        """
        :type link: LinkInfo
        """
        links = [FileInfoResponse(f.folder, f.path, f.name) for f in link.links]

        return LinkInfoResponse(
            link.folder,
            link.path,
            link.name,
            links
        )

