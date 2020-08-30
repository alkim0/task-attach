#!/usr/bin/env python

from setuptools import setup

setup(
    name="task-attach",
    version="0.1.0",
    packages=["task_attach"],
    description="Scripts to manage attachments in taskwarrior",
    author="Albert Kim",
    author_email="alkim@alkim.org",
    install_requires=["pyyaml", "tasklib"],
    scripts=[
        "bin/task-attach-new",
        "bin/task-attach-open",
        "bin/task-attach-add",
        "bin/mutt2task",
        "bin/open-via-mutt",
    ],
)
