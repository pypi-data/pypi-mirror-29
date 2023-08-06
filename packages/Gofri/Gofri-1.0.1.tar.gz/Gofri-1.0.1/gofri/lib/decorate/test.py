from gofri.lib.decorate.decorator import Decorator

class Greeter(Decorator):
    """Greet return value of decorated function."""
    def setup(self, greeting='hello'):
        super(Greeter, self).setup()
        self.greeting = greeting

    def run(self, *args, **kwargs):
        """Run decorated function and return modified result."""
        name = super(Greeter, self).run(*args, **kwargs)
        return '{greeting} {name}!'.format(greeting=self.greeting, name=name)




@Greeter
def world():
    return "world"

if __name__ == '__main__':
    print(world())