import errno
import importlib
import json
import logging
import os
import sys

import click

from . import const, SchemaRegistry, SchemaFactory

_CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command(context_settings=_CONTEXT_SETTINGS)
@click.option("-dr", "--dry-run", is_flag=True, help="Prints basic diagnostic information and exits.")
@click.option("-l", "--log-level", default=30, help="Sets the logging level. Default: 30 (Warning).")
@click.option("-no-pk/-pk", "--ignore-primary/--require-primary", default=True,
              help="Decision to include primary keys in schema. Default: Ignored")
@click.option("-no-fk/-fk", "--ignore-non-nullable-foreign/--require-non-nullable-foreign", default=False,
              help="Decision to include non-nullable foreign keys in schema. Default: Required")
@click.option("-no-fk-null/-fk-null", "--ignore-nullable-foreign/--require-nullable-foreign", default=False,
              help="Decision to include nullable foreign keys in schema. Default: Required")
@click.option("--depth", default=0, help="How deep to recurse into the provided module. Default: 0.")
@click.option("-o", "-out", "--output-dir", type=click.Path(exists=False, file_okay=False),
              help=""""Output directory. Will be created if it doesn't exist. 
              If not provided, output goes to console with schemas separated by a newline.""")
@click.option("-f", "--name-format", default="{{{}}}.schema.json".format(const.CLASS_NAME_LOWER_KEY),
              help="""Format string to determine the filename. 
              
              Supported keywords are: {0}, {1}, {2}.
              
              Default: {{{1}}}.schema.json
              """.format(const.CLASS_NAME_KEY, const.CLASS_NAME_LOWER_KEY, const.MODULE_NAME_KEY))
@click.argument("SOURCE")
def cli_main(dry_run, log_level, ignore_primary, ignore_non_nullable_foreign, ignore_nullable_foreign,
             depth, output_dir, name_format, source):
    """
    JSONIO CLI to generate schemas for the module or class provided in SOURCE.

    SOURCE can be a module (eg. my_app.model) or a specific class (eg. my_app.model:MyClass).
    """
    _init_logging(log_level)
    registry = SchemaRegistry(schema_factory=SchemaFactory(ignore_primary=ignore_primary,
                                                           ignore_foreign_non_nullable=ignore_non_nullable_foreign,
                                                           ignore_foreign_nullable=ignore_nullable_foreign))
    if ':' not in source:
        target_module = source
        registry.register_module(importlib.import_module(target_module), depth=depth)
    else:
        try:
            target_module, target_class = source.split(':')
        except ValueError:
            click.echo("Couldn't separate out module and class names. Did you put in too many ':' symbols?")
            sys.exit(-1)
        module_ = importlib.import_module(target_module)
        try:
            registry.register_class(getattr(module_, target_class))
        except AttributeError:
            click.echo("Couldn't find class '{}' in module '{}'".format(target_class, target_module))
            sys.exit(-2)
    if dry_run:
        click.echo("Mapped classes: {}".format(sorted(list(registry.keys()))))
        sys.exit(0)
    if output_dir:
        _make_directory(output_dir)
        for cls, schema in iter(registry.items()):
            format_values = {const.CLASS_NAME_KEY: cls.__name__, const.CLASS_NAME_LOWER_KEY: cls.__name__.lower(),
                             const.MODULE_NAME_KEY: cls.__module__}
            target_path = os.path.normpath(os.path.join(output_dir, name_format.format(**format_values)))
            with open(target_path, "wt") as file_:
                click.echo("Schema for '{}' in file '{}'".format(cls, target_path))
                file_.write(json.dumps(schema, sort_keys=True, indent=2))
    else:  # Output to stdout
        for cls, schema in iter(registry.items()):
            click.echo(json.dumps(schema, sort_keys=True, indent=2))
            click.echo("")


def _make_directory(dir_path):
    try:
        os.makedirs(dir_path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(dir_path):
            pass
        else:
            raise


def _init_logging(level):
    root_logger = logging.getLogger("sqlalchemy_jsonio")
    root_logger.setLevel(level)
    console_out = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s :: %(message)s",
                                  datefmt="%H:%M:%S")
    console_out.setFormatter(formatter)
    root_logger.addHandler(console_out)


if __name__ == "__main__":
    cli_main()
