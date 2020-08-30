#!/usr/bin/env python
"""
Script to add new annotations to task. 
"""

import argparse
import re
import os
import subprocess
import sys
import uuid

from tasklib import TaskWarrior

from .config import Config
from .utils import select_task, FILE


def get_args():
    parser = argparse.ArgumentParser(description="Adds a new random file to a task")
    parser.add_argument("-e", "--editor", help="Uses $EDITOR by default")
    parser.add_argument(
        "-t", "--ext", default="txt", help="Specify an extension for new file"
    )
    parser.add_argument("id_or_filter")
    parser.add_argument("comments", nargs="*")
    return parser.parse_args()


def _main():
    args = get_args()
    if args.editor:
        editor = args.editor
    elif "EDITOR" in os.environ:
        editor = os.environ["EDITOR"]
    else:
        raise Exception("Set an editor")
    config = Config()
    path = os.path.join(config.task_attach_dir, "{}.{}".format(uuid.uuid4(), args.ext))
    subprocess.run(editor + " " + path, shell=True, check=True)

    tw = TaskWarrior(config.task_home)
    task = select_task(tw, args.id_or_filter)

    annotation = "{}:{}".format(FILE, path)
    if args.comments:
        annotation = " ".join(args.comments) + " " + annotation
    task.add_annotation(annotation)


def main():
    try:
        _main()
    except Exception as e:
        print(e)
        sys.exit(2)
