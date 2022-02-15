from djclick.adapter import CommandAdapter
from wq.build import Config


def as_django_command(command):
    class Command(CommandAdapter):
        def __init__(self, *args, **kwargs):
            self.__dict__.update(command.__dict__)
            for param in self.params:
                if param.required:
                    param.required = False

        def make_context(self, *args, **kwargs):
            ctx = super().make_context(*args, **kwargs)
            ctx.obj = Config.from_file()
            return ctx

    return Command
