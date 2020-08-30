from .menu import Menu

FILE = "file"
MAIL = "mail"
URL = "url"

# def quote_spec(spec):
#     if re.search(r"\s", spec):
#         if '"' in spec and "'" in spec:
#             quoted_spec = spec
#         elif '"' in spec:
#             quoted_spec = "'{}'".format(spec)
#         else:
#             quoted_spec = '"{}"'.format(spec)
#     else:
#         quoted_spec = spec
#     return quoted_spec


def select_task(tw, id_or_filter):
    """
    Here, tw is a TaskWarrior instance
    """
    tasks = tw.tasks.filter(id_or_filter)
    if len(tasks) == 1:
        task = tasks[0]
    elif len(tasks) > 1:
        menu = Menu(tasks)
        i = menu.show_and_pick()
        task = tasks[i]
    else:
        raise Exception("No task matched given filter")

    return task
