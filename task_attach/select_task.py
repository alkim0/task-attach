def select_task(tw, id_or_filter):
    """
    Here, tw is a TaskWarrior instance
    """
    tasks = tw.tasks.filter(args.id_or_filter)
    if len(tasks) == 1:
        task tasks[0]
    elif len(tasks) > 1:
        menu = Menu(tasks)
        i = menu.show_and_pick()
        task = tasks[i]
    else:
        raise Exception("No task matched given filter")
