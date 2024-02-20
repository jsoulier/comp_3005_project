import psycopg

import contextlib
import glob
import json
import os
import subprocess

class DB:
    OB_NAME_       = 'football'
    OB_REPOSITORY_ = 'https://github.com/statsbomb/open-data'
    OB_COMMIT_     = '0067cae166a56aa80b2ef18f61e16158d6a7359a'
    DB_NAME_       = 'comp_3005_project'
    DB_USERNAME_   = 'postgres'
    DB_PASSWORD_   = 'password'

    def __init__(self):
        try:
            self.open_()
        except Exception as e:
            print(e)

    def load(self):
        try:
            self.download_()
            # self.load_('', lambda x: '')
        except Exception as e:
            print(e)

    @contextlib.contextmanager
    def cd_(self, path):
        previous = os.getcwd()
        os.chdir(path)
        try:
            yield
        finally:
            os.chdir(previous)

    def open_(self):
        self.connection = psycopg.connect(
            'dbname={name} '
            'user={username} '
            'password={password} '
            .format(
                name=self.DB_NAME_,
                username=self.DB_USERNAME_,
                password=self.DB_PASSWORD_
            )
        )

    def download_(self):
        if os.path.exists(self.OB_NAME_):
            return
        subprocess.run([
            'git',
            'clone',
            '--single-branch',
            self.OB_REPOSITORY_,
            self.OB_NAME_
        ])
        with self.cd_(self.OB_NAME_):
            subprocess.run([
                'git',
                'reset',
                '--hard',
                self.OB_COMMIT_
            ])

    def load_(self, name, function):
        search = os.path.join(self.OB_NAME_, 'data', name, '**', '*.json')
        for path in glob.glob(search, recursive=True):
            try:
                with open(path, 'r', encoding='utf-8') as file:
                    function(json.load(file))
            except Exception as e:
                print(e)

if __name__ == '__main__':
    db = DB()
    db.load()
