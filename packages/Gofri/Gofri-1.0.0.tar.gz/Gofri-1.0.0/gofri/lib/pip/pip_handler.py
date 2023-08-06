import importlib
import os


def check_pname(name):
    #TODO: check if package is available
    if " " in name or name is "":
        return False
    return True

class PIPHandler():
    def __init__(self):
        self.package_names = []

    def get_uninstalled_packages(self):
        result = []
        if self.package_names is not None:
            for pname in self.package_names:
                spec = importlib.util.find_spec(pname)
                if spec is None:
                    result.append(pname)
        return result


    def install(self):
        for package_name in self.get_uninstalled_packages():
            if check_pname(package_name):
                print("Installing missing dependency: \"{}\" ...".format(package_name))
                print("> FLASK: ", end="")
                os.system("sudo -S pip install " + package_name)