from clinodes.nodes import ArgNode

from gofri.lib.project_generator.module_generator import generate_module
from gofri.lib.project_generator.templates import build_entity_file

data = {}

class ModuleGeneratorNode(ArgNode):
    def setup(self):
        self.expects_more = True
        self.enable_any = True

    def run(self, *args_remained):
        name = args_remained[0]
        inner_path = args_remained[1]
        generate_module(
            root_package_path=data["root"],
            module_package=inner_path,
            name=name
        )

class ControllerGeneratorNode(ArgNode):
    def setup(self):
        self.expects_more = False
        self.enable_any = True

    def run(self, *args_remained):
        name = args_remained[0]
        inner_path = "{}.back.controller".format(data["root_base"])
        generate_module(
            root_package_path=data["root"],
            module_package=inner_path,
            name=name
        )


class ModelGeneratorNode(ArgNode):
    def setup(self):
        self.expects_more = False
        self.enable_any = True

    def run(self, *args_remained):
        name = args_remained[0]
        inner_path = "{}.back.model".format(data["root_base"])
        generate_module(
            root_package_path=data["root"],
            module_package=inner_path,
            name=name
        )


class ServiceGeneratorNode(ArgNode):
    def setup(self):
        self.expects_more = False
        self.enable_any = True

    def run(self, *args_remained):
        name = args_remained[0]
        inner_path = "{}.back.service".format(data["root_base"])
        generate_module(
            root_package_path=data["root"],
            module_package=inner_path,
            name=name
        )


class EntityGeneratorNode(ArgNode):
    def setup(self):
        self.expects_more = False
        self.enable_any = True

    def run(self, *args_remained):
        name = args_remained[0]
        cols = args_remained[1::]
        print(cols)
        inner_path = "{}.back.entity".format(data["root_base"])
        generate_module(
            root_package_path=data["root"],
            module_package=inner_path,
            name=name,
            template=build_entity_file(data["root"], name, cols)
        )


class GenerateNode(ArgNode):
    def setup(self):
        self.commands = {
            "module" : ModuleGeneratorNode,
            "controller": ControllerGeneratorNode,
            "model": ModelGeneratorNode,
            "service": ServiceGeneratorNode,
            "entity": EntityGeneratorNode
        }
        self.expects_more = True

class RootNode(ArgNode):
    def setup(self):
        self.commands = {
            "generate": GenerateNode,
        }
        self.expects_more = True