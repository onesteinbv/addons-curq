import os
import shutil
import sys
from os import listdir, path

import click


@click.command()
@click.option(
    "--location", help="Location of git repository on file system", required=True
)
@click.option("--package-file", help="Package file name")
@click.option("--destination", help="Destination", required=True)
def main(location, package_file, destination):
    if not package_file:
        package_file = path.join(location, "package.txt")

    if not path.exists(package_file):
        return click.echo("Package file not found at `%s`" % package_file, err=True)

    if path.exists(destination):
        shutil.rmtree(destination)
    os.makedirs(destination, exist_ok=True)

    module_locs = []
    with open(package_file, "r") as package_fh:
        lines = package_fh.readlines()
        for line in lines:
            line = line.strip()
            if not line:
                continue
            module_loc = path.join(location, line)
            module_name = line.split("/")[-1]
            if module_name == "*":
                # Loop over modules
                modules_dir = "/".join(module_loc.split("/")[:-1])
                modules_dir_list = listdir(modules_dir)
                for module_name in modules_dir_list:
                    module_dir = path.join(modules_dir, module_name)
                    if not path.isdir(module_dir):
                        continue
                    manifest_loc = path.join(module_dir, "__manifest__.py")
                    if not path.exists(manifest_loc):
                        continue
                    module_locs.append(module_dir)
                    shutil.copytree(module_dir, path.join(destination, module_name))
                continue
            if not path.exists(module_loc):
                click.echo("Module not found at `%s`" % module_loc, err=True)
                sys.exit(1)
            module_locs.append(module_loc)
            shutil.copytree(module_loc, path.join(destination, module_name))


if __name__ == "__main__":
    main()
