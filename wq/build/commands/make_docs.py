from wq.build import wq
import click


DOC_LAYOUT = """wq {name}
{title_line}

wq {name}: {short_help}
Provided by [{mod}].

```shell
$ wq {name} --help

{help}
```

[{mod}]: ./index.md"""

INDEX_LAYOUT = """---
order: -1
---

wq
==

The wq command line interface provides a number of utilities for creating and
deploying applications with the wq framework.

```shell
$ wq --help

{help}
```

## Commands

Command | Module | Description
--------|--------|-------------"""
INDEX_ROW = "[{name}] | [{mod}] | {short_help}"
LINK_ROW = "[{name}]: ../{mod}/{name}.md"


@wq.command(hidden=True)
@click.pass_context
def make_docs(ctx):
    command_list = []
    modules = set()
    for i, (name, cmd) in enumerate(sorted(wq.commands.items())):
        if cmd.hidden:
            continue

        mod = ".".join(cmd.callback.__module__.split(".")[:2])
        if not mod.startswith("wq."):
            continue

        modules.add(mod)

        with open("%s/%s.md" % (mod, name), "w") as f:
            cctx = click.Context(cmd, info_name=name, parent=ctx.parent)
            command_info = dict(
                name=name,
                title_line="=" * (len(name) + 3),
                short_help=cmd.get_short_help_str(),
                mod=mod,
                help=cmd.get_help(cctx),
            )
            print(DOC_LAYOUT.format(**command_info), file=f)
            command_list.append(command_info)

    wq_help = wq.get_help(ctx.parent).split("Commands:")[0].strip()
    with open("wq.build/cli.md", "w") as f:
        print(INDEX_LAYOUT.format(help=wq_help), file=f)
        for command_info in command_list:
            print(INDEX_ROW.format(**command_info), file=f)
        print("", file=f)
        for mod in sorted(modules):
            print("[{mod}]: ../{mod}/index.md".format(mod=mod), file=f)
        for command_info in command_list:
            print(LINK_ROW.format(**command_info), file=f)
