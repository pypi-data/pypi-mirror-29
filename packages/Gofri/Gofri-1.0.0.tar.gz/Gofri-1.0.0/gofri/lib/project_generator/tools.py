import os


def get_project_name(name):
    root_package = ""
    for char in str(name):
        if char.isalnum():
            root_package += char
        else:
            root_package += "_"
    return root_package.lower()


def is_python_package(path):
    files = os.listdir(path)
    return "__init__.py" in files

def init_python_package(path):
    os.makedirs(path, exist_ok=True)
    open("{}/__init__.py".format(path), "w")

def make_python_packages(path_to_root_package, packages):
    if is_python_package(path_to_root_package):
        package_names = packages.split(".")
        if package_names[0] == os.path.basename(path_to_root_package):
            cur_path = ""
            for name in package_names[1::]:
                cur_path += "/{}".format(name)
                fullpath = "{}{}".format(path_to_root_package, cur_path)
                if os.path.exists(fullpath):
                    if not is_python_package(fullpath):
                        open("{}/__init__.py".format(fullpath), "w")
                else:
                    os.mkdir(fullpath)
                    open("{}/__init__.py".format(fullpath), "w")
    else:
        raise ValueError("Given root path is not a python package")

