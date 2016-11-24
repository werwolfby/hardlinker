import os
from hardlinker.linker import Linker, FolderInfo
from tests import downloads_dir, shows_dir


def test_get_all_files():
    linker = Linker([], [], ['mp4', 'mkv'])
    downloads_folder_info = FolderInfo('Downloads', downloads_dir)
    files = linker._get_all_files(downloads_folder_info)

    assert len(files) == 5

    assert files[0].folder == downloads_folder_info
    assert files[0].path == []
    assert files[0].size == 57
    assert files[0].name == 'American.Horror.Story.S06E01.720p.WEB.rus.LostFilm.TV.mp4'
    assert files[0].abs_path == os.path.join(downloads_dir, 'American.Horror.Story.S06E01.720p.WEB.rus.LostFilm.TV.mp4')

    assert files[1].folder == downloads_folder_info
    assert files[1].path == ['Black Mirror', 'Season 1']
    assert files[1].size == 38
    assert files[1].name == 'Black.Mirror.s01e01.HDTVRip.720p.mkv'
    assert files[1].abs_path == os.path.join(downloads_dir, 'Black Mirror', 'Season 1',
                                             'Black.Mirror.s01e01.HDTVRip.720p.mkv')

    assert files[2].folder == downloads_folder_info
    assert files[2].path == ['Black Mirror', 'Season 2']
    assert files[2].size == 40
    assert files[2].name == 'Black.Mirror.s02e01.HDTVRip.720p.mkv'
    assert files[2].abs_path == os.path.join(downloads_dir, 'Black Mirror', 'Season 2',
                                             'Black.Mirror.s02e01.HDTVRip.720p.mkv')

    assert files[3].folder == downloads_folder_info
    assert files[3].path == ['TBBT']
    assert files[3].size == 36
    assert files[3].name == 'TBBT.[S10E01].HD720p.KB.[qqss44].mkv'
    assert files[3].abs_path == os.path.join(downloads_dir, 'TBBT', 'TBBT.[S10E01].HD720p.KB.[qqss44].mkv')

    assert files[4].folder == downloads_folder_info
    assert files[4].path == ['TBBT']
    assert files[4].size == 36
    assert files[4].name == 'TBBT.[S10E02].HD720p.KB.[qqss44].mkv'
    assert files[4].abs_path == os.path.join(downloads_dir, 'TBBT', 'TBBT.[S10E02].HD720p.KB.[qqss44].mkv')


def test_get_links():
    downloads_folder_info = FolderInfo('Downloads', downloads_dir)
    shows_folder_info = FolderInfo('Shows', shows_dir)
    linker = Linker([downloads_folder_info], [shows_folder_info], ['mp4', 'mkv'])
    linker.update_links()

    links = {l.name: l for l in linker.links}

    ahsS06E01 = links['American.Horror.Story.S06E01.720p.WEB.rus.LostFilm.TV.mp4']
    bmS0101 = links['Black.Mirror.s01e01.HDTVRip.720p.mkv']
    bmS0201 = links['Black.Mirror.s02e01.HDTVRip.720p.mkv']
    tbbtS1001 = links['TBBT.[S10E01].HD720p.KB.[qqss44].mkv']
    tbbtS1002 = links['TBBT.[S10E02].HD720p.KB.[qqss44].mkv']

    assert len(ahsS06E01.links) == 1
    assert len(bmS0101.links) == 1
    assert len(bmS0201.links) == 0
    assert len(tbbtS1001.links) == 1
    assert len(tbbtS1002.links) == 1
