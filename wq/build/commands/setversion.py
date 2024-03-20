from wq.build import wq
import click
import re
import pathlib


@wq.command()
@click.option(
    "--filename",
    "-f",
    default="version.txt",
    help="Name of text file (default is version.txt)",
)
@click.option("--esm", help="Name of an ESM module (e.g. myapp/version.js)")
@click.option("--package", help="Path to package.json")
@click.argument("version")
@wq.pass_config
def setversion(config, **conf):
    """
    Update version.txt (and version.js).  Useful for keeping track of which
    version has been deployed.  The version.js ESM module can be referenced
    within your application to notify users.
    """
    base_path = config.path.parent if config.path else pathlib.Path()
    version_path = base_path / conf["filename"]
    if conf["version"] is None:
        if version_path.exists():
            version = version_path.read_text().strip()
        else:
            version = ""
    else:
        version = conf["version"]
        version_path.write_text(version)

    if conf["esm"]:
        # Update version.js
        js_file = base_path / conf["esm"]
        js_tmpl = """export default "%s";"""
        js_file.write_text(js_tmpl % version)
        click.echo("%s: %s" % (js_file.relative_to(base_path), version))
    else:
        click.echo("Application version: %s" % version)

    if conf["package"]:
        package_path = base_path / conf["package"]
        content = package_path.read_text()
        content = re.sub(
            '"version": "[^"]+"', '"version": "%s"' % version, content
        )
        package_path.write_text(content)

    return version
