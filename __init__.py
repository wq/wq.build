import click
import yaml

# Core CLI
@click.group()
@click.option(
    '-c', '--config',
    default='wq.yml',
    help='Path to configuration file (default is wq.yml).'
)
@click.pass_context
def wq(ctx, config):
    """
    wq is a suite of command line utilities for building citizen science apps.
    """
    try:
        conf = yaml.load(open(config))
    except IOError:
        conf = {}
    ctx.obj = conf

# Load custom commands from other modules
from pkg_resources import iter_entry_points
module_names = []
for module in iter_entry_points(group='wq', name=None):
    module_names.append(module.name)
    module.load()

# Update help text with list of installed modules
wq.help += " Installed modules: " + ", ".join(sorted(module_names))
