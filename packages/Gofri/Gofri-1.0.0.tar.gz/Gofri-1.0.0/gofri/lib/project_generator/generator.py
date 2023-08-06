import os

from gofri.lib.project_generator.templates import *
from gofri.lib.project_generator.tools import get_project_name, make_python_packages, init_python_package


def generate_start_file(root_package, name):
    with open("{}/{}".format(root_package, "start.py"), "w") as start_file:
        start_file.write(build_start_file_content(get_project_name(name)))

def generate_modules_file(root_package, name):
    with open("{}/{}".format(root_package, "modules.py"), "w") as xml_file:
        pass

def generate_generate_file(root_package, name):
    with open("{}/{}".format(root_package, "generate.py"), "w") as gen_file:
        gen_file.write(generator_file_content)


def generate_xml(root_package, name):
    with open("{}/{}".format(root_package, "conf.xml"), "w") as xml_file:
        xml_file.write(build_xml(root_package, name))

def generate_web_dir(root_package):
    make_python_packages(root_package, "{}.web".format(os.path.basename(root_package)))

def generate_back_dir(root_package):
    make_python_packages(root_package, "{}.back.controller".format(os.path.basename(root_package)))

def generate_project(path, name, web=True, back=True, db=True, orm=True, custom_xml=False):
    root_package_name = get_project_name(name)
    root_package = "{}/{}/{}".format(path, name, root_package_name)

    init_python_package(root_package)

    generate_xml(root_package, name)
    generate_start_file(root_package, name)
    generate_modules_file(root_package, name)
    generate_generate_file(root_package, name)

    if web:
        generate_web_dir(root_package)
    if back:
        generate_back_dir(root_package)