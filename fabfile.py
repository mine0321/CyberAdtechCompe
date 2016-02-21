from fabric.api import sudo
from fabric.api import run
from fabric.api import env
from fabric.api import cd

env.hosts = [
    "52.69.144.199",
    "52.192.29.19",
    "52.69.107.193",
    "52.69.254.131",
    "52.192.59.135",
]
env.user = 'ec2-user'

def deploy():
    pull()
    restart()

def pull():
    with cd("/var/www/adtech_compe_f"):
        sudo('git pull')

def restart():
    sudo('supervisorctl stop tornado')
    sudo('pkill python')
    sudo('supervisorctl start tornado')

def stop():
    sudo('supervisorctl stop tornado')
    sudo('pkill python')

def start():
    sudo('supervisorctl start tornado')

def checkout(branch='master'):
    with cd("/var/www/adtech_compe_f"):
        sudo('git checkout {}'.format(branch))
