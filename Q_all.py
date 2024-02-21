import datetime
import subprocess
import sys

import database

def time(function, name):
    print('[' + name + '] ', end='', flush=True)
    t1 = datetime.datetime.now()
    function()
    t2 = datetime.datetime.now()
    d1 = int((t2 - t1).seconds)
    d2 = int((t2 - t1).microseconds / 1000)
    print(str(d1) + '.' + str(d2) + 's')

time(database.sparse_download, 'sparse_download')
time(database.open_database, 'open_database')
time(database.create_tables, 'create_tables')
time(database.populate_tables, 'populate_tables')
time(database.quit_database, 'quit_database')

for i in range(1, 11):
    path = 'Q_' + str(i) + '.py'
    time(lambda: subprocess.run(sys.executable + ' ' + path), path)
