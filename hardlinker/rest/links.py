from hardlinker.linker import Linker, FileInfo, LinkInfo, FolderInfo
from falcon import HTTPBadRequest


class LinkItResource(object):
    def __init__(self, linker):
        """
        :type linker: Linker
        """
        self.linker = linker

    def on_get(self, req, resp):
        self.linker.update_links()
        links = self.linker.links

        resp.json = [self.create_link_response(l) for l in links]

    def on_post(self, req, resp):
        folder = req.get_param('folder', required=True)
        file_path = req.get_param('path', required=True)

        file_info_dict = req.json
        if 'folder' not in file_info_dict or 'path' not in file_info_dict or 'name' not in file_info_dict:
            raise HTTPBadRequest('body miss required fields', 'body have to have folder, path and name properties')

        path = file_path.split('/')
        name = path[-1]

        folder_info = self.linker.get_folder(folder)
        if folder_info is None:
            raise HTTPBadRequest('can\'t find folder', 'folder {0} doens\'t exist'.format(folder))

        link_folder = self.linker.get_folder(file_info_dict['folder'])
        if link_folder is None:
            raise HTTPBadRequest('can\'t find folder', 'folder {0} doens\'t exist'.format(file_info_dict['folder']))

        file_info = FileInfo(folder_info, path[0:-1], name)
        link_info = FileInfo(link_folder, file_info_dict['path'], file_info_dict['name'])

        self.linker.link(file_info, link_info)

        resp.json = file_info_dict

    @staticmethod
    def create_link_response(link):
        """
        :type link: LinkInfo
        """
        resp = LinkItResource.create_file_info_response(link)

        resp['links'] = [LinkItResource.create_file_info_response(l) for l in (link.links or [])]

        return resp

    @staticmethod
    def create_file_info_response(info):
        """
        :type info: FileInfo
        """
        return {
            'folder': info.folder.name,
            'path': info.path or [],
            'name': info.name
        }


class LinkAllResource(object):
    def __init__(self, linker):
        """
        :type linker: Linker
        """
        self.linker = linker

    def on_post(self, req, resp):
        links = [LinkInfo.from_json(j, self.linker) for j in req.json]

        result = []

        for link in links:
            if link.links is not None and len(link.links) > 0:
                file_info = self.linker.get_link(link.folder, link.path, link.name)

                self.linker.link(file_info, link.links[0])
                file_info.links.append(link.links[0])

                result.append(file_info)

        resp.json = [LinkItResource.create_link_response(l) for l in result]
