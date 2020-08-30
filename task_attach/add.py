#!/usr/bin/env python
"""
Script to add annotations to task. 
"""

import argparse
import re
import os
import sys

from tasklib import TaskWarrior

from .config import Config
from .utils import select_task, FILE, MAIL, URL


def get_args():
    parser = argparse.ArgumentParser(description="Adding a new attachment to a task")
    parser.add_argument("-t", "--type", choices=(FILE, MAIL, URL))
    parser.add_argument("id_or_filter")
    parser.add_argument("spec")
    parser.add_argument("comments", nargs="*")
    return parser.parse_args()


def determine_type(type_, spec):
    if type_:
        return type_
    else:
        file_path = os.path.expandvars(os.path.expanduser(spec))
        if os.path.exists(file_path):
            return FILE

        if spec.startswith("<") and spec.endswith(">"):
            return MAIL

        if re.match(r"https?://", spec):
            return URL

        if "@" in spec:
            return MAIL

        if "." in spec:
            return URL

        raise Exception("Could not determine type of spec")


def add(id_or_filter, type_, spec, comments):
    config = Config()
    tw = TaskWarrior(config.task_home)
    task = select_task(tw, id_or_filter)

    type_ = determine_type(type_, spec)
    if type_ == URL and not re.match(r"https?://", spec):
        spec = "http://" + spec
    annotation = "{}:{}".format(type_, spec)
    if comments:
        annotation = " ".join(comments) + " " + annotation
    task.add_annotation(annotation)


def main():
    try:
        args = get_args()
        add(args.id_or_filter, args.type, args.spec, args.comments)
    except Exception as e:
        print(e)
        sys.exit(2)
