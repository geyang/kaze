from collections import defaultdict

import click

from kaze.file_utils import load_yml, write_yml


@click.group(invoke_without_command=True)
@click.pass_context
def kaze(ctx):
    if ctx.invoked_subcommand is None:
        click.echo('Hello! This is the Kaze CLI.')
        config = load_yml(".kaze.yml")
        print(config)


@kaze.command()
@click.argument("name", default="")
@click.argument("source", default="")
@click.option("--path", '-o', default=None, help="target location for the dataset")
@click.option("--verbose", "-v", is_flag=True, help="Verbose mode")
def add(name, source, path, verbose, **kwargs):
    print(f"adding {name} from {source}", kwargs)
    config = load_yml(".kaze.yml") or defaultdict(list)
    print(config)
    new_entry = dict(name=name, source=source, path=path)
    print(new_entry)
    config['datasets'].append(new_entry)
    write_yml({**config}, ".kaze.yml")


@kaze.command()
@click.argument("name", default="")
@click.argument("source", default="")
@click.option("--path", '-o', default=None, help="target location for the dataset")
@click.option("--verbose", "-v", is_flag=True, help="Verbose mode")
def check(name, source, path, verbose, **kwargs):
    print(f"adding {name} from {source}", kwargs)
    config = load_yml(".kaze.yml") or defaultdict(list)
    print(config)
    new_entry = dict(name=name, source=source, path=path)
    print(new_entry)
    config['datasets'].append(new_entry)
    write_yml({**config}, ".kaze.yml")


@kaze.command()
@click.argument("source", default="")
@click.argument("output", default="")
@click.argument("format", default="")
@click.option("--verbose", "-v", is_flag=True, help="Verbose mode")
def get(source, output, format, verbose, **kwargs):
    print(f"getting from {source} to {output}", kwargs)
