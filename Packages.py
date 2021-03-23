import subprocess
import sys


def installPackages(pacakge):
    subprocess.check_call([sys.executable, "-m", "pip", "install", pacakge])


if __name__ == '__main__':
    installPackages('unittest2')
    installPackages('selenium')

