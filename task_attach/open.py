#!/usr/bin/env python
"""
Script to open a task.
"""

import argparse
import os
import re
import subprocess
import sys

from tasklib import TaskWarrior

from .config import Config
from .menu import Menu
from .utils import select_task, FILE, URL, MAIL


def get_args():
    parser = argparse.ArgumentParser(
        description="Opens an annotation attachment with given command"
    )
    parser.add_argument(
        "-x",
        "--cmd",
        help="Command to prepend to open the attachment. By default, uses $EDITOR for files, xdg-open for urls, and errors if cmd is not given for mails. The prepended file:/url:/mail: is removed before given as an argument to the given command",
    )
    parser.add_argument("id_or_filter")
    return parser.parse_args()


def get_default_cmd(config, type_):
    if type_ == FILE:
        if "EDITOR" in os.environ:
            return os.environ["EDITOR"]
        else:
            raise Exception("$EDITOR unset")
    elif type_ == URL:
        return "xdg-open"
    elif type_ == MAIL:
        return config.mail_open_cmd
    else:
        raise Exception("Must specify cmd for this type: {}".format(type_))


def _main():
    args = get_args()
    config = Config()
    tw = TaskWarrior(config.task_home)
    task = select_task(tw, args.id_or_filter)
    attachments = [
        a
        for a in task["annotations"]
        if re.search(r"({}):\S+".format("|".join((FILE, URL, MAIL))), str(a))
    ]
    if len(attachments) == 1:
        attachment = str(attachments[0])
    elif len(attachments) > 1:
        menu = Menu(attachments)
        attachment = str(attachments[menu.show_and_pick()])
    else:
        raise Exception("No valid attachments")

    file_beg = attachment.rfind("{}:".format(FILE))
    url_beg = attachment.rfind("{}:".format(URL))
    mail_beg = attachment.rfind("{}:".format(MAIL))
    if file_beg >= 0:
        type_ = FILE
        spec = os.path.expandvars(
            os.path.expanduser(attachment[file_beg + len(FILE) + 1 :])
        )
    elif url_beg >= 0:
        type_ = URL
        spec = attachment[url_beg + len(URL) + 1 :]
    elif mail_beg >= 0:
        type_ = MAIL
        spec = attachment[mail_beg + len(MAIL) + 1 :]
    else:
        raise Exception("wtf")

    cmd = args.cmd if args.cmd else get_default_cmd(config, type_)

    subprocess.run('{} "{}"'.format(cmd, spec), shell=True, check=True)


def main():
    try:
        _main()
    except Exception as e:
        print(e)
        sys.exit(2)
