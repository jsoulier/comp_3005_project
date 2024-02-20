import psycopg

import contextlib
import functools
import glob
import json
import shutil
import os
import subprocess
import stat

UPSTREAM = 'https://github.com/statsbomb/open-data' 
COMMIT = '0067cae166a56aa80b2ef18f61e16158d6a7359a'
DATABASE = 'football'
USERNAME = 'football'
PASSWORD = 'password'

# All of the seasons required to complete the queries
SEASONS = [
    '2003/2004',
    '2018/2019',
    '2019/2020',
    '2020/2021',
]

@contextlib.contextmanager
def cd(path):
    previous = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(previous)

def force_cwd(function):
    @functools.wraps(function)
    def _(*args, **kwargs):
        path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(path)
        return function(*args, **kwargs)
    return _

@force_cwd
def open_database():
    pass

@force_cwd
def sparse_download():
    if os.path.exists('json'):
        return

    # Start with basic metadata
    subprocess.run([
        'git',
        'clone',
        '-n',
        '--filter=tree:0',
        UPSTREAM,
        'json'
    ])

    with cd('json'):

        # Clone the root to determine what matches are required
        subprocess.run([
            'git',
            'sparse-checkout',
            'set',
            '--no-cone',
            'data/competitions.json'
        ])
        subprocess.run([
            'git',
            'checkout',
            COMMIT
        ])

        # Clone the required matches
        path = os.path.join('data', 'competitions.json')
        with open(path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        paths = []
        for item in data:
            if item['season_name'] not in SEASONS:
                continue
            competition = str(item['competition_id'])
            season = str(item['season_id'])
            paths.append('data/matches/' + competition + '/' + season + '.json')
        subprocess.run([
            'git',
            'sparse-checkout',
            'add',
            '--no-cone',
        ] + paths)

if __name__ == '__main__':
    open_database()
    sparse_download()








# class DB:
#     OD_NAME_       = 'football'
#     OD_REPOSITORY_ = 'https://github.com/statsbomb/open-data'
#     OD_COMMIT_     = '0067cae166a56aa80b2ef18f61e16158d6a7359a'
#     DB_NAME_       = 'comp_3005_project'
#     DB_USERNAME_   = 'postgres'
#     DB_PASSWORD_   = 'password'

#     def __init__(self):
#         try:
#             self.open_()
#         except Exception as e:
#             print(e)

#     def load(self):
#         try:
#             self.download_()
#             # self.load_('', lambda x: '')
#         except Exception as e:
#             print(e)

#     @contextlib.contextmanager
#     def cd_(self, path):
#         previous = os.getcwd()
#         os.chdir(path)
#         try:
#             yield
#         finally:
#             os.chdir(previous)

#     def open_(self):
#         self.connection = psycopg.connect(
#             'dbname={name} '
#             'user={username} '
#             'password={password} '
#             .format(
#                 name=self.DB_NAME_,
#                 username=self.DB_USERNAME_,
#                 password=self.DB_PASSWORD_
#             )
#         )

#     def download_(self):
#         if os.path.exists(self.OD_NAME_):
#             return
#         subprocess.run([
#             'git',
#             'clone',
#             '--single-branch',
#             self.OD_REPOSITORY_,
#             self.OD_NAME_
#         ])
#         with self.cd_(self.OD_NAME_):
#             subprocess.run([
#                 'git',
#                 'reset',
#                 '--hard',
#                 self.OD_COMMIT_
#             ])

#     def load_(self, name, function):
#         search = os.path.join(self.OD_NAME_, 'data', name, '**', '*.json')
#         for path in glob.glob(search, recursive=True):
#             try:
#                 with open(path, 'r', encoding='utf-8') as file:
#                     function(json.load(file))
#             except Exception as e:
#                 print(e)

# if __name__ == '__main__':
#     db = DB()
#     db.load()
