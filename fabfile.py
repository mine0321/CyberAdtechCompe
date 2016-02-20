from fabric.api import sudo
from fabric.api import run
from fabric.api import env
from fabric.api import cd

env.hosts = ["52.69.144.199"]
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
