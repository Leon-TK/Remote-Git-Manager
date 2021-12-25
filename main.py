import subprocess
import sys
import time
from getpass import getpass

# Ensure that your and remote default shell is Powershell

# SSH host url
# I dont need "ssh://"" and "port" because they are setted in config (c:\users\user\.ssh\config)
HOST="192.168.100.4"

# Remote environment variable contains path to folder where git repos are will be created.
REMOTE_GIT_ENV = "GIT_BARE_REPOS"

# Local environment variable contains path to folder where clone repos are will be cloned to.
LOCAL_GIT_ENV = "GIT_REMOTE_REPOS"

# Name of project. Remote git folder name
PROJECT_NAME = "Remote git managment scripts"

# Set this to false if you set no key phrase for your ssh key
USE_KEYPHRASE = True

# Keyphrase of ssh key.
gSshKeyPhrase = ""

def ShellSshProcess(host):
    # Use shell = true because we need powershell comandlets, not ssh. You hae to be ensure that local and remote uese powershell as default shell
    return subprocess.Popen(["ssh", f"{host}"], stdin=subprocess.PIPE, stdout = subprocess.PIPE, universal_newlines = True, bufsize = 0, shell = True)

def PowershellProcess():
    # Use shell = false because powershell is a shell
    return subprocess.Popen(["powershell"], stdin=subprocess.PIPE, stdout = subprocess.PIPE, universal_newlines = True, bufsize = 0, shell = False)

def GetGitFolderPath(process):
    process.stdin.write(f"$env = Get-ChildItem -Path Env:\{REMOTE_GIT_ENV}\n")
    process.stdin.write("$value = $env.value\n")
    """ process.stdin.write("$value\n")
    buffer = process.stdout.readlines()
    print(buffer[len(buffer) - 1]) """

def ChangeDirToGit(process):
    process.stdin.write("cd \"$value\"\n")

def CreateProjectFolder(process):
    process.stdin.write(f"New-Item -Path . -Name \"{PROJECT_NAME}.git\" -ItemType \"directory\"\n")
    process.stdin.write(f"$path = \"$value\" + \"\{PROJECT_NAME}.git\"\n")
    process.stdin.write("cd $path\n")

def CreateBareRepository(process):
    process.stdin.write("git init --bare\n")

def Exit(process):
    process.stdin.write("exit\n")

def GetLocalGitPath(process):
    process.stdin.write(f"$env = Get-ChildItem -Path Env:\{LOCAL_GIT_ENV}\n")
    process.stdin.write("$value = $env.value\n")

def ChangeDirToLocalGit(process):
    process.stdin.write("cd \"$value\"\n")

def CloneRemoteRepo(process):
    #TODO: have to get git remote path from shell to paste there "D:\git\"
    process.stdin.write(f"git clone \"{HOST}:D:\git\{PROJECT_NAME}.git\"\n")
    if USE_KEYPHRASE:
        #Sleep for password input appears
        time.sleep(5)
        process.stdin.write(f"{gSshKeyPhrase}\n")

def PrintBuffer(process, header):
    print('\n' + header + '\n')
    result = process.stdout.readlines()
    if result == []:
        error = process.stderr.readlines()
        print >> sys.stderr, f"ERROR: {error}"
    else:
        print (result)

def CreateRemoteRepository():
    ssh = ShellSshProcess(HOST)
    GetGitFolderPath(ssh)
    ChangeDirToGit(ssh)
    CreateProjectFolder(ssh)
    CreateBareRepository(ssh)
    Exit(ssh)
    ssh.stdin.close()
    PrintBuffer(ssh, "SSH")

def CreateCloneRepository():
    powershell = PowershellProcess()
    GetLocalGitPath(powershell)
    ChangeDirToLocalGit(powershell)
    CloneRemoteRepo(powershell)
    Exit(powershell)
    powershell.stdin.close()
    PrintBuffer(powershell, "POWERSHELL")

def GetPass():
    gSshPass = input("Enter your SSH keyphrase: ")

if USE_KEYPHRASE: GetPass()
CreateRemoteRepository()
CreateCloneRepository()

