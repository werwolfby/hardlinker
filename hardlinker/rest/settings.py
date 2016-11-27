import os
from hardlinker.linker import Linker, FolderInfo
from abc import ABCMeta, abstractproperty


class SettingsResource(object):
    def on_get(self, req, resp):
        resp.json = {
            'pathSeparator': os.sep
        }


class FoldersResource(object):
    __metaclass__ = ABCMeta

    def __init__(self, linker):
        """
        :type linker: Linker
        """
        self.linker = linker

    @abstractproperty
    def folders(self):
        pass

    def on_get(self, req, resp):
        folders = [InputFoldersResource.create_folder_info_response(f) for f in self.folders]

        resp.json = folders

    @staticmethod
    def create_folder_info_response(folder):
        """
        :type folder: FolderInfo
        """
        return {
            'name': folder.name,
            'path': folder.path
        }


class InputFoldersResource(FoldersResource):
    def __init__(self, linker):
        """
        :type linker: Linker
        """
        super(InputFoldersResource, self).__init__(linker)

    @property
    def folders(self):
        return self.linker.input_folders.values()


class OutputFoldersResource(FoldersResource):
    def __init__(self, linker):
        """
        :type linker: Linker
        """
        super(OutputFoldersResource, self).__init__(linker)

    @property
    def folders(self):
        return self.linker.output_folders.values()
