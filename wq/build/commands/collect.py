import os
import json
import yaml
from wq.build import wq
import click
from collections import OrderedDict


NEST = {
    "json": lambda f: json.load(f),
    "yaml": lambda f: yaml.safe_load(f),
}


def readfiles(basedir, ftype=None, fext=None):
    obj = OrderedDict()
    if fext is None:
        fext = ftype

    for path, dirs, files in sorted(os.walk(basedir)):
        if os.sep + "." in path:
            continue
        o = obj
        if path == basedir:
            path = ""
        else:
            path = path[len(basedir) + 1 :]
            apath = path.split(os.sep)
            for subdir in apath:
                o.setdefault(subdir, OrderedDict())
                o = o[subdir]
            path = os.sep.join(apath) + os.sep

        for filename in sorted(files):
            name, ext = os.path.splitext(filename)
            if ftype and ext != "." + fext:
                continue

            fpath = path + name
            data = open(basedir + os.sep + fpath + ext)
            if ftype in NEST:
                try:
                    o[name] = NEST[ftype](data)
                except ValueError as e:
                    raise click.ClickException(
                        "Could not parse %s; %s" % (fpath + ext, e)
                    )
            else:
                o[name] = data.read()
            data.close()

    return obj


@wq.command()
@click.option(
    "--type", default="json", help="Source file type (e.g. json, yaml)"
)
@click.option("--extension", help="Source file extension (e.g. json, yml)")
@click.option("--output", default="output.json", help="Destination JSON file")
@click.option("--indent", default=4, help="JSON Indentation")
@click.option(
    "--esm/--raw-json", help="Wrap as ES module, or just generate JSON"
)
@click.argument("paths", type=click.Path(exists=True), nargs=-1)
@wq.pass_config
def collectjson(config, **conf):
    """
    Load directory files into a JSON object.  The keys will be the filenames
    (without extentions) and the values will be the file contents.
    The values will be stored as text strings, except when combining JSON or
    YAML files into a single object.  In that case, the file contents will be
    embeded as full JSON objects instead of strings.

    wq collectjson --type json --output config.json config/
    """

    if not conf["extension"]:
        conf["extension"] = conf["type"]

    if not conf["paths"]:
        if isinstance(config.get("collectjson", None), dict):
            # Ensure wq.yml paths are used if not passed via argument
            conf["paths"] = config["collectjson"].get("paths", None)

        if not conf["paths"]:
            conf["paths"] = ["."]

    obj = OrderedDict()
    for d in conf["paths"]:
        obj.update(readfiles(d, conf["type"], conf["extension"]))

    outfile = open(conf["output"], "w")

    opts = {}
    if conf["indent"]:
        opts["indent"] = conf["indent"]

    if conf["esm"]:
        txt = json.dumps(obj, **opts)
        txt = "export default %s;" % txt
        outfile.write(txt)
    else:
        json.dump(obj, outfile, **opts)

    click.echo(
        "%s: %s objects collected from %s"
        % (conf["output"], len(obj), ", ".join(conf["paths"]))
    )

    outfile.close()
