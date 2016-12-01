import os
import sys


if sys.platform == 'win32' and not hasattr(os.path, 'samefile'):
    import ntfsutils.hardlink
    os.path.samefile = ntfsutils.hardlink.samefile
    os.link = ntfsutils.hardlink.create


class FolderInfo(object):
    def __init__(self, name, path):
        self.name = name
        self.path = path

    @property
    def abs_path(self):
        if len(self.path) == 0:
            return ''

        if self.path[0].endswith(':'):
            return os.path.join(self.path[0] + os.sep, *self.path[1:])

        return os.path.join(*self.path)

    @staticmethod
    def from_path(name, path):
        parts = path.split(os.sep)
        return FolderInfo(name, parts)


class ShowsFolderInfo(FolderInfo):
    @staticmethod
    def from_path(name, path):
        parts = path.split(os.sep)
        return ShowsFolderInfo(name, parts)


class MoviesFolderInfo(FolderInfo):
    @staticmethod
    def from_path(name, path):
        parts = path.split(os.sep)
        return MoviesFolderInfo(name, parts)


class FileInfo(object):
    def __init__(self, folder, path, name):
        """
        :type folder: FolderInfo
        """
        self.folder = folder
        self.path = path
        self.name = name
        self.abs_path = os.path.join(self.folder.abs_path, *(self.path + [self.name]))

    @property
    def size(self):
        try:
            return os.path.getsize(self.abs_path)
        except IOError:
            return -1


class LinkInfo(FileInfo):
    def __init__(self, folder, path, name):
        super(LinkInfo, self).__init__(folder, path, name)
        self.links = []

    def add_link(self, link):
        self.links.append(link)


class Linker(object):
    def __init__(self, input_folders, output_folders, extensions):
        self.input_folders = {f.name: f for f in input_folders}
        self.output_folders = {f.name: f for f in output_folders}
        self.extensions = extensions
        self.links = []
        self._input_files = {}
        self._output_files = {}

    def get_folder(self, folder):
        return self.input_folders.get(folder, None) or \
                self.output_folders.get(folder, None)

    def update_links(self):
        def to_size_dict(files):
            result = {}

            for f in files:
                items = result.get(f.size)
                if items is None:
                    items = []
                    result[f.size] = items

                items.append(f)

            return result

        self._input_files = to_size_dict(self._get_all_files(*self.input_folders.values()))
        self._output_files = to_size_dict(self._get_all_files(*self.output_folders.values()))

        self.links = []

        for size, input_files in self._input_files.items():
            for input_file in input_files:
                outputs = self._output_files.get(size)
                link = LinkInfo(input_file.folder, input_file.path, input_file.name)
                if outputs is not None:
                    for output_file in outputs:
                        if os.path.samefile(input_file.abs_path, output_file.abs_path):
                            link.add_link(output_file)

                self.links.append(link)

    def _get_all_files(self, *folders):
        result = []

        for folder_info in folders:
            folder_path = os.sep.join(folder_info.path)

            for root, _, file_names in os.walk(folder_path):
                root_path = root.split(os.sep)
                result = result + [self._get_file_info(folder_info, root_path, file_name)
                                   for file_name in file_names
                                   if self._has_linkable_extension(file_name)]

        return result

    def _has_linkable_extension(self, filename):
        for ext in self.extensions:
            if filename.endswith('.' + ext):
                return True

        return False

    @staticmethod
    def _get_file_info(folder_info, root, filename):
        path = root[len(folder_info.path):]

        return FileInfo(folder_info, path, filename)

    def link(self, source, link_name):
        """
        :type source: FileInfo
        :type link_name: FileInfo
        """
        folder, _ = os.path.split(link_name.abs_path)
        if not os.path.exists(folder):
            os.makedirs(folder)

        os.link(source.abs_path, link_name.abs_path)
