import subprocess
import sys
import time
from getpass import getpass

procecc = subprocess.Popen(["powershell"], stdin=subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE, universal_newlines = True, bufsize = 0, shell = False)

i = procecc.stdin.write("Write-Host \"Hello\"\n")
line = procecc.stdout.readline()
procecc.terminate()

original_stdout = sys.stdout
with open('filename.txt', 'w') as f:
    sys.stdout = f # Change the standard output to the file we created.
    print (i)
    sys.stdout = original_stdout # Reset the standard output to its original value

sys.exit(1)