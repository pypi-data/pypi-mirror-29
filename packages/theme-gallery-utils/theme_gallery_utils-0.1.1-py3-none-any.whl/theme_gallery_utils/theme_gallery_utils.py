# -*- coding: utf-8 -*-

"""
Main module.
"""

import argparse
import json
import logging.config
import os
import shutil
import sys
import tempfile
from . import paths, xml_utils, parsing, git_utils, es_install, capturing, \
    compressing, comparing

logger = logging.getLogger(__name__)


def install():
    """Install and configure emulationstation."""

    es_install.install_dependencies()

    # use a temporary directory for building
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_es_dir = os.path.join(temp_dir, "EmulationStation")

        es_install.clone(temp_es_dir)

        es_install.build(temp_es_dir)

        # ensure bin dir exists and copy over emulationstation binary
        if not os.path.isdir(paths.BIN):
            os.mkdir(paths.BIN)
        shutil.copy(os.path.join(temp_es_dir, "emulationstation"), paths.BIN)

        # copy resources to .emulationstation
        es_resources = os.path.join(paths.EMULATIONSTATION, "resources/")
        if os.path.isdir(es_resources):
            shutil.rmtree(es_resources)
        shutil.copytree(os.path.join(temp_es_dir, "resources"), es_resources)

    es_install.configure(paths.EMULATIONSTATION)


def opml(**kwargs):
    """Turn the esthemes list into an opml file of rss feeds."""
    esthemes = parsing.get_esthemes(**kwargs)
    xml_utils.create_opml_file(esthemes)


def pull(**kwargs):
    """Pull or clone all themes into the themes dir."""
    esthemes = parsing.get_esthemes(**kwargs)
    for theme in esthemes:
        git_utils.pull_or_clone(theme, paths.ESTHEMES)


def capture(**kwargs):
    """Take screenshots of specific or all themes."""

    if not shutil.which("shutter"):
        capturing.install_dependencies()

    # update the release date in the gamelist
    gamelist = os.path.join(
        paths.EMULATIONSTATION, "gamelists/atari2600/gamelist.xml")
    xml_utils.update_gamelist_date(gamelist)

    # get the theme names if passed by file or list
    if kwargs["theme_names"]:
        theme_names = kwargs["theme_names"]
    else:
        theme_names = parsing.get_esthemes_names(**kwargs)

    logger.info("Taking screenshots of {}".format(theme_names))
    capturing.auto(theme_names, paths.UNCOMPRESSED)


def compress():
    """Compress the capturing output dir."""

    if not shutil.which("optipng"):
        compressing.install_dependencies()

    compressing.compress_images(paths.UNCOMPRESSED, paths.COMPRESSED)


def compare():
    """Create histograms between repository images and captured images."""
    comparing.compare_images(
        paths.COMPRESSED, paths.GALLERY, paths.DIFFERENCES)


def parse_arguments(args):
    """Take commandline arguments and parse them."""

    # create and populate parser with arguments
    parser = argparse.ArgumentParser(description="Theme Gallery Utils")
    parser.add_argument("-d", "--debug", action="store_true")

    # create subparsers for the rest of the commands
    subparsers = parser.add_subparsers(dest="command")
    subparsers.required = True

    subparser = subparsers.add_parser(
        "install", help="install and configure emulationstation")
    subparser.set_defaults(func=install)

    subparser = subparsers.add_parser(
        "opml", help="create opml from esthemes")
    subparser.set_defaults(func=opml)
    exclusive_group = subparser.add_mutually_exclusive_group()
    exclusive_group.add_argument("-f", "--file", type=str)
    exclusive_group.add_argument(
       "-t", "--themes", nargs="+", type=str, dest="theme_names")

    subparser = subparsers.add_parser("pull", help="pull all themes")
    subparser.set_defaults(func=pull)
    exclusive_group = subparser.add_mutually_exclusive_group()
    exclusive_group.add_argument("-f", "--file", type=str)
    exclusive_group.add_argument(
       "-t", "--themes", nargs="+", type=str, dest="theme_names")

    subparser = subparsers.add_parser("capture", help="take screenshots")
    subparser.set_defaults(func=capture)
    exclusive_group = subparser.add_mutually_exclusive_group()
    exclusive_group.add_argument("-f", "--file", type=str)
    exclusive_group.add_argument(
        "-t", "--themes", nargs="+", type=str, dest="theme_names")

    subparser = subparsers.add_parser(
        "compress", help="compress new screenshots")
    subparser.set_defaults(func=compress)

    subparser = subparsers.add_parser(
        "compare", help="compare gallery images to new screenshots")
    subparser.set_defaults(func=compare)

    return parser.parse_args(args)


def setup_logging(debug):
    """Replace filename from the logging config and load it."""

    dict_file = os.path.join(paths.BASE, "config/logging_dict.json")
    with open(dict_file, "r") as buf:
        logging_dict = json.load(buf)

    # ensure logging dir exists
    if not os.path.isdir(paths.CACHE):
        os.makedirs(paths.CACHE, exist_ok=True)

    # add file path to the dict
    logging_dict["handlers"]["file"]["filename"] = os.path.join(
        paths.CACHE, "gallery_utils.log")

    if debug:
        logging_dict["handlers"]["file"]["level"] = "DEBUG"
        logging_dict["handlers"]["console"]["level"] = "DEBUG"
    else:
        logging_dict["handlers"]["file"]["level"] = "INFO"
        logging_dict["handlers"]["console"]["level"] = "WARNING"

    logging.config.dictConfig(logging_dict)


def main():
    """Main entry point of gallery utils."""

    # parse commandline arguments
    parsed_args = parse_arguments(sys.argv[1:])

    # setup logging from config
    setup_logging(parsed_args.debug)

    # execute selected method
    logger.info(parsed_args)
    if parsed_args.command in ("opml", "pull", "capture"):
        parsed_args.func(
            file=parsed_args.file, theme_names=parsed_args.theme_names)
    else:
        parsed_args.func()


if __name__ == "__main__":
    main()
