from django.core.management.base import BaseCommand
from django.core.management import call_command
from wq.build import Config
import subprocess
import os

if os.name == "nt":
    NPM_COMMAND = "npm.cmd"
else:
    NPM_COMMAND = "npm"


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = Config.from_file()

    def add_arguments(self, parser):
        parser.add_argument("version")

    def handle(self, *args, **options):
        version = options.get("version")
        self.call_command_with_config("setversion", version)
        self.call_command_with_config("dump_config", rel_path=True)
        self.call_command_with_config("icons")
        self.npm_build()
        call_command("collectstatic", interactive=False)
        self.call_command_with_config("movefiles")
        self.call_command_with_config("serviceworker", version)

    def call_command_with_config(self, name, *args, rel_path=False):
        if name not in self.config:
            return
        conf = self.config[name]
        if "filename" in conf and rel_path:
            conf["filename"] = self.config.path.parent / conf["filename"]
        call_command(name, *args, **conf)

    def npm_build(self):
        root_dir = self.config.path.parent
        app_dir = root_dir / "app"
        if app_dir.exists() and (app_dir / "package.json").exists():
            subprocess.check_call([NPM_COMMAND, "run", "build"], cwd=app_dir)
        elif (root_dir / "package.json").exists():
            subprocess.check_call([NPM_COMMAND, "run", "build"], cwd=root_dir)
