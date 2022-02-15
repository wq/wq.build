from wq.build.commands import serviceworker
from ._base import as_django_command


Command = as_django_command(serviceworker)
