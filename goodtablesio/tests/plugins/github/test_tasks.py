from unittest import mock

from goodtablesio.plugins.github import tasks


def test_get_job_conf_url():

    clone_url = 'https://github.com/my-org/my-repo.git'

    expected_url = \
        'https://raw.githubusercontent.com/my-org/my-repo/master/goodtables.yml'
    assert tasks._get_job_conf_url(clone_url) == expected_url


def test_get_job_conf_url_custom_branch():

    clone_url = 'https://github.com/my-org/my-repo.git'

    expected_url = \
        'https://raw.githubusercontent.com/my-org/my-repo/fix/goodtables.yml'
    assert tasks._get_job_conf_url(clone_url, branch='fix') == expected_url


def test_get_job_files():

    with mock.patch('os.walk') as mock_walk:
        '''
        This mocks the following file structure:

            /my/folder/.git/file0.txt
            /my/folder/folder1/ (empty)
            /my/folder/folder2/file1.csv
            /my/folder/folder2/file2.pdf
            /my/folder/folder3/folder4/file3.pdf
            /my/folder/folder3/folder4/file4.csv
            /my/folder/folder3/folder4/file5.csv
            /my/folder/file6.csv
            /my/folder/file7.txt
        '''

        mock_walk.return_value = [
            ('/my/folder', ['.git', 'folder1', 'folder2', 'folder3'],
                ['file6.csv', 'file7.txt']),
            ('/my/folder/folder1', [], []),
            ('/my/folder/folder2', [], ['file1.csv', 'file2.pdf']),
            ('/my/folder/folder3', ['folder4'], []),
            ('/my/folder/folder3/folder4', [],
                ['file3.pdf', 'file4.csv', 'file5.csv']),
        ]

        assert tasks._get_job_files('/my/folder') == [
            'file6.csv',
            'file7.txt',
            'folder2/file1.csv',
            'folder2/file2.pdf',
            'folder3/folder4/file3.pdf',
            'folder3/folder4/file4.csv',
            'folder3/folder4/file5.csv',
        ]
