import subprocess
import sys

for i in range(1, 11):
    subprocess.run(sys.executable + ' Q_' + str(i) + '.py')
