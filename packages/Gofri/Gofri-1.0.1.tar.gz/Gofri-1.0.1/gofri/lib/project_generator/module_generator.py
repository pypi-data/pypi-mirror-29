import os


def is_python_package(path):
    files = os.listdir(path)
    return "__init__.py" in files

def make_python_packages(path_to_root_package, packages):
    if is_python_package(path_to_root_package):
        package_names = packages.split(".")
        if path_to_root_package[-1] == "/":
            path_to_root_package = path_to_root_package[0:-1:]
        if package_names[0] == os.path.basename(path_to_root_package):
            cur_path = ""
            fullpath = ""
            for name in package_names[1::]:
                cur_path += "/{}".format(name)
                fullpath = "{}{}".format(path_to_root_package, cur_path)
                if os.path.exists(fullpath):
                    if not is_python_package(fullpath):
                        open("{}/__init__.py".format(fullpath), "w")
                else:
                    os.mkdir(fullpath)
                    open("{}/__init__.py".format(fullpath), "w")
            return fullpath
    else:
        raise ValueError("Given root path is not a python package")


def create_import_statement(root_package_path, project_path, name):
    package = str(project_path).replace("/", ".")
    parent = os.path.basename(os.path.normpath(root_package_path))
    import_statement = "from {} import {}".format(package, name)
    return import_statement


def generate_module(root_package_path, module_package, name, template=""):
    package_path = make_python_packages(root_package_path, module_package)
    with open("{}/{}.py".format(package_path, name), "w") as module_file:
        module_file.write(template)

    with open("{}/modules.py".format(root_package_path), "a") as modules_py:
        modules_py.write(
            "\n{}".format(
                create_import_statement(root_package_path, module_package, name)
            )
        )