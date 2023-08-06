from clinodes.nodes import ArgNode, Switch

verbose = False

class AddingNode(ArgNode):
    def setup(self):
        self.commands = {
            "person",
            "pet"
        }
        self.enable_any = False
        self.expects_more = False

    def run(self, *args_remained):
        print(args_remained[1])
        print("Adding a new {}")


class RemovingNode(ArgNode):
    pass


class VerboseSwitch(Switch):
    def setup(self):
        self.expects_more = True

    def run(self, *args):
        verbose = True


class RootNode(ArgNode):
    def setup(self):
        self.commands = {
            "add": AddingNode,
            "remove": RemovingNode
        }
        self.switches = {
            "--verbose", VerboseSwitch
        }
        self.expects_more = True

if __name__ == '__main__':
    RootNode()