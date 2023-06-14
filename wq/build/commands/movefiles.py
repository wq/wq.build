from wq.build import wq
import click
import pathlib


@wq.command()
@click.argument("source", type=click.Path(), nargs=-1)
@click.argument("dest", type=click.Path())
@wq.pass_config
def movefiles(config, source, dest):
    """
    Move one or more files to a different folder.
    Useful for e.g. elevating htdocs/static/app/public/*.* to htdocs/*.*
    after running ./manage.py collectstatic.
    """

    base_path = config.path.parent if config.path else pathlib.Path()
    dest_path = base_path / dest
    dest_path.mkdir(parents=True, exist_ok=True)

    if not source and "movefiles" in config:
        source = config["movefiles"].get("source")

    if not isinstance(source, (list, tuple)):
        source = [source]

    for src in source:
        for path in base_path.glob(src):
            path.replace(dest_path / path.name)
