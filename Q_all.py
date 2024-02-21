import subprocess
import sys

import database

database.sparse_download()
database.open_database()
database.create_tables()
database.populate_tables()
database.quit_database()

for i in range(1, 11):
    subprocess.run(sys.executable + ' Q_' + str(i) + '.py')
