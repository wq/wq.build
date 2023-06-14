from wq.build.commands import movefiles
from ._base import as_django_command


Command = as_django_command(movefiles)
