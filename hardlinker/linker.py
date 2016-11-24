import os
import sys


if sys.platform == 'win32' and not hasattr(os.path, 'samefile'):
    import ntfsutils.hardlink
    os.path.samefile = ntfsutils.hardlink.samefile


class FolderInfo(object):
    def __init__(self, name, path):
        self.name = name
        self.path = path


class FileInfo(object):
    def __init__(self, folder, path, name):
        self.folder = folder
        self.path = path
        self.name = name
        self.abs_path = os.path.join(self.folder.path, *(self.path + [self.name]))

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
            for root, _, filenames in os.walk(folder_info.path):
                result = result + [self._get_file_info(folder_info, root, filename)
                                   for filename in filenames
                                   if self._has_linkable_extension(filename)]

        return result

    def _has_linkable_extension(self, filename):
        for ext in self.extensions:
            if filename.endswith('.' + ext):
                return True

        return False

    @staticmethod
    def _get_file_info(folder_info, root, filename):
        rel = root[len(folder_info.path):]
        path = rel.split(os.sep)
        size = os.path.getsize(os.path.join(root, filename))

        return FileInfo(folder_info, path[1:] if len(path) > 0 else [], filename)
