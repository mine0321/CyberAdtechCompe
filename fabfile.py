from fabric.api import sudo
from fabric.api import run
from fabric.api import env
from fabric.api import cd

env.hosts = ["52.69.144.199"]
env.usre = 'root'

def move_to_app():
    with cd("/var/www/adtech_compe_f"):
        run('pwd')