import shutil

import pkg_resources

from flask import Flask
from flask_restful import Api

from gofri.lib.conf.config_reader import ConfigReader
from gofri.lib.pip.pip_handler import PIPHandler

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relation, sessionmaker


ROOT = ""
ROOT_PATH = ""

C = ConfigReader(ROOT_PATH)

CONF = None
HOST = None
PORT = None
DATABASE_RDBMS = None
MYSQL_CONFIG = None
DEPENDENCIES = None


def init_config():
    global CONF, HOST, PORT, DATABASE_RDBMS, MYSQL_CONFIG, DEPENDENCIES

    CONF = C.get_conf_xml()["configuration"]
    HOST = C.get_dict_config(CONF, "hosting", "host")
    PORT = C.get_dict_config(CONF, "hosting", "port")
    DATABASE_RDBMS = C.get_dict_config(CONF, "database", "rdbms")
    MYSQL_CONFIG = C.get_dict_config(CONF, "database", "mysql-config")
    DEPENDENCIES = C.get_dict_config(CONF, "dependencies", "dependency")

    if isinstance(DEPENDENCIES, str):
        DEPENDENCIES = [DEPENDENCIES]


APP = Flask(__name__)
API = Api(APP)


Base = declarative_base()



def run():
    global HOST
    if HOST == None:
        HOST = "127.0.0.1"
    APP.run(port=int(PORT), host=HOST)


def main(root_path, modules):
    banner = "GOFRI -- version: {}\n{}\n".format(
        pkg_resources.get_distribution("gofri").version,
        "#"*shutil.get_terminal_size().columns
    )
    print(banner)

    global C, ROOT_PATH
    C = ConfigReader(root_path)
    ROOT_PATH = root_path

    init_config()
    piphandler = PIPHandler()
    piphandler.package_names = DEPENDENCIES

    piphandler.install()
    print("All required dependencies are installed")

    run()