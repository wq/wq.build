from wq.build.commands import setversion
from ._base import as_django_command


Command = as_django_command(setversion)
