import os
from collections import defaultdict
from pathlib import Path

import click
from params_proto.neo_proto import Proto, ParamsProto
from termcolor import cprint

from kaze.curl_utils import download
from kaze.file_utils import load_yml, write_yml, get_md5, decompress, is_archive
from kaze.utils import include, omit


class Envs(ParamsProto, cli=False):
    KAZE_DATA_DIR = Proto(env='KAZE_DATA_DIR', default='$HOME/datasets')
    DATA_DIR = Proto(env='DATA_DIR', default=KAZE_DATA_DIR.value)


class NamedList(dict):
    def add(self, name, **entry):
        self[name] = dict(name=name, **entry)

    def filter_by(self, *keys):
        return [include(entry, *keys) for entry in self.to_list()]

    def from_list(self, entries):
        for entry in entries:
            self.add(**entry)

    def to_list(self):
        return list(self.values())


class KazeConfig:
    datasets = None

    def load(self):
        config = load_yml(".kaze.yml") or defaultdict(list)
        config_lock = load_yml(".kaze-lock.yml") or defaultdict(list)

        self.datasets = NamedList()
        for entry in [*config['datasets'], *config_lock['datasets']]:
            self.datasets.add(**entry)

        self.config = omit(config, "datasets")

    def save(self):
        write_yml(dict(datasets=self.datasets.filter_by("name", "source"), **self.config),
                  ".kaze.yml")
        write_yml(dict(datasets=self.datasets.to_list()), ".kaze-lock.yml")


@click.group(invoke_without_command=True)
@click.pass_context
def kaze(ctx):
    if ctx.invoked_subcommand is None:
        kaze_config = KazeConfig()
        kaze_config.load()

        n = len(kaze_config.datasets)
        if n:
            print(f"Found {n} dataset{'s' if n > 1 else ''}.")
        else:
            print("No datasets found")

        # todo: read from .kaze.yml instead
        # todo: add new entries to .kaze.yml
        for entry in kaze_config.datasets.to_list():
            if not os.path.exists(entry['path']):
                cprint(f"{entry['name']} is missing", "red")
                download(entry['source'], entry['archive_path'])
                if is_archive(entry['archive_path']):
                    decompress(entry['archive_path'], entry['path'])
                    os.remove(entry['archive_path'])


@kaze.command()
@click.argument("source", default="")
@click.option("--name", '-n', default=None)
@click.option("--path", '-o', default=None, help="target location for the dataset")
@click.option("--quiet", "-q", is_flag=True, help="Verbose mode")
@click.option("--unzip", "-z", is_flag=True, help="Decompress the dataset")
# @click.option("--remove_archive", "-z", is_flag=True, help="Decompress the dataset")
@click.option("--verbose", "-v", is_flag=True, help="Verbose mode")
def add(source, name, path, quiet, unzip, verbose, **kwargs):
    kaze_config = KazeConfig()
    kaze_config.load()

    if name is None:
        name = Path(source).stem
        print(f"Using the name {name}")

    if path is None:
        path = Envs.DATA_DIR + "/" + name

    # todo: ask to overwrite/download again if the dataset already exists
    if name in kaze_config.datasets:
        answer = input(f"{name} has already been added. Update? [Y/n]") or "Y"
        if answer.lower() == "n":
            print('Exiting...')
            return

    cprint(f"adding {name} from {source}. Download to {path}", "blue")

    archive_path = path + Path(source).suffix

    if os.path.exists(archive_path):
        cprint(f"{name} already exists", "red")
        answer = input(f"Remove {path} and download again? [Y/n]") or "Y"
        if answer.lower() == "y":
            os.remove(archive_path)
            print(f"Downloading {name} to {path}") or "Y"
            download(source, archive_path)
    elif quiet:
        print(f"Downloading {name} to {path}") or "Y"
        download(source, archive_path)
    else:
        answer = input(f"Download the file to {path}? [Y/n]") or "Y"
        if answer.lower() == "y":
            download(source, archive_path)

    # load again since the config files might have changed.
    kaze_config.load()
    kaze_config.datasets.add(name=name, source=source, archive_path=archive_path,
                             hash=get_md5(archive_path), path=path)

    if unzip or is_archive(archive_path):
        decompress(archive_path, path)
        # if remove_archive:
        os.remove(archive_path)

    kaze_config.save()


@kaze.command(name="list")
def list_command():
    kaze_config = KazeConfig()
    kaze_config.load()

    for entry in kaze_config.datasets.values():
        print(f"{entry['name']} at {entry['path']}")
