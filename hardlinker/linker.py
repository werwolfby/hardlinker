import os
import sys
import re


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
        parts = FolderInfo.split_path(path)
        return FolderInfo(name, parts)

    @staticmethod
    def split_path(path):
        drive, path = os.path.splitdrive(path)
        if path.startswith(os.sep):
            path = path[len(os.sep):]
        if path.startswith(os.altsep):
            path = path[len(os.altsep):]

        result_path = []

        while True:
            path, folder = os.path.split(path)
            result_path.append(folder)

            if path == "":
                break

        result_path.reverse()

        return [drive] + result_path


class ShowsFolderInfo(FolderInfo):
    class ShowInfo(object):
        def __init__(self, show, seasons):
            self.show = show
            self.seasons = seasons

    _season_match = re.compile(u'^Season\s+(?P<number>\d+)$', re.IGNORECASE)
    """
    :type _shows: dict[string, dict[string, string]]
    """
    _shows = dict()

    def read_shows(self):
        root = self.abs_path

        shows = {}

        for show in os.listdir(root):
            show_folder = os.path.join(root, show)
            if not os.path.isdir(show_folder):
                continue

            seasons = {}

            for season in os.listdir(show_folder):
                season_folder = os.path.join(show_folder, season)
                if not os.path.isdir(season_folder):
                    continue

                match = self._season_match.match(season)
                if match is None:
                    continue

                number = int(match.group('number'))
                seasons[number] = season

            shows[show.lower()] = self.ShowInfo(show, seasons)

        self._shows = shows

    def find_show(self, show, season):
        show_info = self._shows.get(show.lower(), None)
        if show_info is None:
            return show, 'Season {0}'.format(season)

        season_info = show_info.seasons.get(season, None)
        if season_info is None:
            return show_info.show, 'Season {0}'.format(season)

        return show_info.show, season_info

    @staticmethod
    def from_path(name, path):
        parts = FolderInfo.split_path(path)
        return ShowsFolderInfo(name, parts)


class MoviesFolderInfo(FolderInfo):
    @staticmethod
    def from_path(name, path):
        parts = FolderInfo.split_path(path)
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

    @staticmethod
    def from_json(json, linker):
        """
        :type json: dict
        :type linker: Linker
        """
        folder_name = json['folder']
        folder = linker.get_folder(folder_name)
        if folder is None:
            raise KeyError("Can't find folder: {0}".format(folder_name))

        return FileInfo(folder, json['path'], json['name'])


class LinkInfo(FileInfo):
    def __init__(self, folder, path, name):
        super(LinkInfo, self).__init__(folder, path, name)
        self.links = []

    def add_link(self, link):
        self.links.append(link)

    @staticmethod
    def from_json(json, linker):
        """
        :type json: dict
        :type linker: Linker
        """
        folder_name = json['folder']
        folder = linker.get_folder(folder_name)
        if folder is None:
            raise KeyError("Can't find folder: {0}".format(folder_name))

        link_info = LinkInfo(folder, json['path'], json['name'])
        for link in json['links']:
            link_info.add_link(FileInfo.from_json(link, linker))
        return link_info


class Linker(object):
    """
    :type links: list[LinkInfo]
    """

    def __init__(self, input_folders, output_folders, extensions):
        self.input_folders = {f.name: f for f in input_folders}
        self.output_folders = {f.name: f for f in output_folders}
        self.extensions = extensions
        self.links = []
        self._input_files = {}
        self._output_files = {}

    def get_folder(self, folder):
        return self.input_folders.get(folder, None) or self.output_folders.get(folder, None)

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
                root_path = FolderInfo.split_path(root)
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

    def get_link(self, folder, path, name):
        for link in self.links:
            if link.folder == folder and link.name == name and self._path_equal(link.path, path):
                return link

        return None

    @staticmethod
    def _path_equal(p1, p2):
        return len(p1) == len(p2) and all([p1[i] == p2[i] for i in range(len(p1))])

    def link(self, source, link_name):
        """
        :type source: FileInfo
        :type link_name: FileInfo
        """
        folder, _ = os.path.split(link_name.abs_path)
        if not os.path.exists(folder):
            os.makedirs(folder)

        os.link(source.abs_path, link_name.abs_path)
