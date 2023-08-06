# -*- coding: utf-8 -*-

"""
Module contains methods for capturing theme screenshots.
"""

import logging
import os
import re
import subprocess
import time
from . import paths

logger = logging.getLogger(__name__)


def shutter_args(theme_name, screenshots_dir):
    """Return args to be used to launch shutter."""
    output_file = os.path.join(screenshots_dir, theme_name + ".png")
    args = [
        "shutter",
        "--window=emulationstation",
        "--no_session",
        "--exit_after_capture",
        "--output={}".format(output_file),
    ]
    return args


def emulationstation_args(theme_name):
    """Return args to be used to launch emulationstation."""

    odd_resolutions = {
        ("320", "240"): ("art-book-pocket", "tft"),
        ("640", "480"): (
            "gbz35",
            "gbz35-dark",
            "minilumi",
            "pixel-tft",
            "simpler-turtlemini",
        ),
        ("1440", "1080"): ("art-book-4-3", "ComicBook_4-3"),
    }

    for resolution in odd_resolutions:
        if theme_name in odd_resolutions[resolution]:
            width, height = resolution
            break
    else:
        width, height = "1920", "1080"

    logger.info("{} at {}x{}".format(theme_name, width, height))

    return [
        "emulationstation",
        "--no-splash",
        "--windowed",
        "--resolution",
        width,
        height,
    ]


def update_es_settings(theme_name, gamelist=False):
    """Update es_config to store the desired theme as default."""
    settings_file = os.path.join(paths.EMULATIONSTATION, "es_settings.cfg")

    # regex pattern for substituting values in es_settings
    settings_regex = r"""
    ("{}"[ ]value=")  # use python substitution for element name, store this
    [^"]*           # match anything but double quote for value
    (")             # match and store closing value quote
    """

    with open(settings_file, "r+") as buf:
        settings_text = buf.read()

        settings_text = re.sub(
            settings_regex.format("ThemeSet"),
            r"\1{}\2".format(theme_name),
            settings_text,
            flags=re.VERBOSE,
        )
        settings_text = re.sub(
            settings_regex.format("StartupSystem"),
            r"\1{}\2".format("atari2600" if gamelist else ""),
            settings_text,
            flags=re.VERBOSE,
        )

        buf.seek(0)
        buf.truncate()
        buf.write(settings_text)


def auto(theme_names, screenshots_dir):
    """Capture screenshots for all themes in the list."""

    # ensure screenshots dir exists
    if not os.path.isdir(screenshots_dir):
        os.makedirs(screenshots_dir, exist_ok=True)

    for theme_name in theme_names:

        # capture system view
        update_es_settings(theme_name)
        es_process = subprocess.Popen(
            emulationstation_args(theme_name),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        time.sleep(1)
        subprocess.run(
            shutter_args(theme_name, screenshots_dir),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        es_process.terminate()

        # capture gamelist view
        update_es_settings(theme_name, gamelist=True)
        es_process = subprocess.Popen(
            emulationstation_args(theme_name),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        time.sleep(1)
        subprocess.run(
            shutter_args(theme_name + "-gamelist", screenshots_dir),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        es_process.terminate()


def install_dependencies(verbose=True):
    """Install shutter as a dependency."""

    args = [
        "sudo",
        "apt-get",
        "install",
        "shutter",
    ]
    kwargs = {"check": True}
    if not verbose:
        kwargs.update(stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    return subprocess.run(args, **kwargs).returncode
