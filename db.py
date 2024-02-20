import psycopg

import contextlib
import json
import os
import subprocess

class DB:
    FOOTBALL_PATH_       = 'football'
    FOOTBALL_REPOSITORY_ = 'https://github.com/statsbomb/open-data'
    FOOTBALL_COMMIT_     = '0067cae166a56aa80b2ef18f61e16158d6a7359a'
    DATABASE_NAME_       = 'comp_3005_project'
    DATABASE_USERNAME_   = 'postgres'
    DATABASE_PASSWORD_   = 'password'

    def __init__(self):
        try:
            self.open_()
        except Exception as e:
            print(e)

    def download(self):
        try:
            self.download_()
        except Exception as e:
            print(e)

    def load(self):
        pass

    @staticmethod
    @contextlib.contextmanager
    def cd_(directory):
        previous = os.getcwd()
        os.chdir(directory)
        try:
            yield
        finally:
            os.chdir(previous)

    def open_(self):
        self.connection = psycopg.connect(
            'dbname={database} '
            'user={username} '
            'password={password} '
            .format(
                database=self.DATABASE_NAME_,
                username=self.DATABASE_USERNAME_,
                password=self.DATABASE_PASSWORD_
            )
        )

    def download_(self):
        if os.path.exists(self.FOOTBALL_PATH_):
            pass
        subprocess.run([
            'git',
            'clone',
            '--depth',
            '1',
            '--single-branch',
            self.FOOTBALL_REPOSITORY_,
            self.FOOTBALL_PATH_
        ])
        with self.cd_(self.FOOTBALL_PATH_):
            subprocess.run([
                'git',
                'checkout',
                self.FOOTBALL_COMMIT_
            ])

if __name__ == '__main__':
    db = DB()
    db.download()
    db.load()
