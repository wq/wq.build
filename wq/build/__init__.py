import click
from .decorators import config_group
import yaml
from pkg_resources import iter_entry_points
import pathlib


# Core wq CLI
@config_group()
@click.option(
    "-c",
    "--config",
    default="wq.yml",
    type=click.Path(path_type=pathlib.Path),
    help="Path to configuration file (default is wq.yml).",
)
@click.pass_context
def wq(ctx, config):
    """
    wq is a suite of command line utilities for building offline GIS apps.
    Each of the commands below can be configured by creating a wq.yml file in
    the current directory.  Many of the commands can also be configured via
    command line options.
    """
    if ctx.obj is not None:
        # Allow for multiple invocations without resetting context
        return

    conf = Config.from_file(config, allow_empty=True)
    ctx.obj = conf
    ctx.default_map = conf


class Config(dict):
    path = None
    filename = None

    @classmethod
    def from_file(cls, path=None, allow_empty=False):
        if path is None:
            path = pathlib.Path("wq.yml")
        data = None
        try:
            with path.open() as f:
                data = yaml.safe_load(f)
        except IOError:
            if not path.is_absolute() and str(path) == "wq.yml":
                for parent in path.absolute().parents:
                    try:
                        with (parent / "wq.yml").open() as f:
                            data = yaml.safe_load(f)
                    except IOError:
                        pass
                    else:
                        path = parent / "wq.yml"
                        break
                if data is None:
                    if allow_empty:
                        click.echo(
                            "Warning: no wq.yml in current or containing directories."
                        )
                        data = {}
                    else:
                        raise
            else:
                raise

        conf = Config(data)
        conf.path = path
        conf.filename = str(path)
        return conf

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if isinstance(self.get("icons", {}).get("size"), str):
            self["icons"]["size"] = [self["icons"]["size"]]


wq.pass_config = click.make_pass_decorator(Config)


# Load custom commands from other modules
module_names = []
for module in iter_entry_points(group="wq", name=None):
    module_names.append(module.name)
    module.load()

expected = [
    "wq.app",
    "wq.build",
    "wq.create",
    "wq.db",
]
missing = set(expected) - set(module_names)

# Update help text with list of installed modules
if module_names:
    wq.help += "\n\n    Installed modules: " + ", ".join(sorted(module_names))
if missing:
    wq.help += "\n\n    Missing modules: " + ", ".join(sorted(missing))
    wq.help += " (try installing the 'wq' metapackage)"
