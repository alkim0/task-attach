import os
import textwrap

import yaml

CONFIG_HOME = os.environ.get("XDG_CONFIG_HOME", os.path.expanduser("~/.config"))

os.makedirs(os.path.join(CONFIG_HOME, "task-attach"), exist_ok=True)
CONFIG_PATH = os.path.join(CONFIG_HOME, "task-attach", "config.yaml")


class Config(object):
    def __init__(self):
        self.data = {}

        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH) as f:
                self.data = yaml.load(f, yaml.FullLoader)

        self.data.setdefault("task_home", "~/.task")
        self.data.setdefault("task_attach_dir", "~/tasknotes")
        self.data.setdefault("mail_open_cmd", "open-via-mutt -m neomutt")

        if not os.path.exists(CONFIG_PATH):
            self._create_initial()

        if not os.path.isdir(self.data["task_attach_dir"]):
            os.makedirs(
                os.path.expandvars(os.path.expanduser(self.data["task_attach_dir"])),
                exist_ok=True,
            )

    @property
    def task_home(self):
        return self.data["task_home"]

    @property
    def task_attach_dir(self):
        return self.data["task_attach_dir"]

    @property
    def mail_open_cmd(self):
        return self.data["mail_open_cmd"]

    def _create_initial(self):
        """
        Used to create an initial version of the config.
        if os.
        """
        initial_config = textwrap.dedent(
            """\
            ---
            # Home address of taskwarrior
            task_home: {task_home}
            # Folder for newly created attachments
            task_attach_dir: {task_attach_dir}
            # Default email open command
            mail_open_cmd: {mail_open_cmd}
            """
        ).format_map(self.data)

        with open(CONFIG_PATH, "w") as f:
            f.write(initial_config)
