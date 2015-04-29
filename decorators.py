import click


class ConfigGroup(click.Group):
    """
    Custom config-aware command Group to allow executing the same subcommand
    multiple times with different configurations.
    """
    def invoke(self, ctx):
        click.Command.invoke(self, ctx)
        cmd_name, cmd, args = self.resolve_command(ctx, ctx.args)
        confs = ctx.default_map.get(cmd_name, {})
        if isinstance(confs, list):
            for conf in confs:
                ctx.default_map[cmd_name] = conf
                last_result = super(ConfigGroup, self).invoke(ctx)
            return last_result
        else:
            return super(ConfigGroup, self).invoke(ctx)


def config_group(name=None, **attrs):
    attrs.setdefault('cls', ConfigGroup)
    return click.command(name, **attrs)
