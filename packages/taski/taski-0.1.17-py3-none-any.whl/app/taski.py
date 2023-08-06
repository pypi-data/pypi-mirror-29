#coding: utf-8

import os
import sys
import time
import yaml
import logging as log
from datetime import datetime
import coloredlogs
from math import floor

from app.planner import PriorityPlanner
import app.todoist_wrapper as todoist_wrapper
import app.elo as elo


def get_config(args):
    try:
        fs = open(args.config)
    except IOError as e:
        log.error("Can't open config file: %s\n" % args.config)
        raise e

    cfg = yaml.load(fs)
    fs.close()
    # TODO validate config
    # keys in config file:
    # email:
    # password:
    # plan_skip_projects:
    # rank_skip_projects:
    # timezone:  # https://pypi.python.org/pypi/tzlocal
    return cfg


def get_app(cfg):

    app = todoist_wrapper.Todoist()
    app.init(cfg)

    return app


def show_old_tasks(app, args, cfg):
    tasks = app.get_tasks()
    tasks = sorted(tasks, key=lambda x: x.ts_added)
    now = datetime.now()
    for t in tasks:
        delta = (now - t.ts_added).days
        if delta > 180:
            print(delta, "days\t", t)


def show_completed_tasks(app, args, cfg):
    tasks = app.get_completed_tasks(since=args.since, until=args.until)
    tasks = sorted(tasks, key=lambda x: x.ts_done)
    for t in tasks:
        print(t.ts_done, t)


def show(app, args, cfg):
    if args.show_cmd == "api_token":
        print(app.get_token())
    elif args.show_cmd == "stats":
        print(app.get_stats())
    elif args.show_cmd == "config":
        print(yaml.dump(cfg))
    elif args.show_cmd == "old_tasks":
        show_old_tasks(app, args, cfg)
    elif args.show_cmd == "completed_tasks":
        show_completed_tasks(app, args, cfg)


def rank(app, args, cfg):
    projects = app.get_projects()
    use_ui = args.tui

    for p in projects:
        if p.name in cfg["rank_skip_projects"]:
            log.debug("Skip project (Skipped due to config): " + p.name)
            continue
        if args.project is not None and p.name != args.project:
            log.debug("Skip project (Name not match): " + p.name)
            continue
        print(p.name, "[", len(p.tasks), "]")
        if use_ui:
            tasks = elo.sort(p.tasks, cmp=elo.tui_cmp)
        else:
            tasks = elo.sort(p.tasks)
        p.tasks = tasks
        # app.update_project(p)

        i = 0
        for t in p.tasks:
            app.update_task(t, item_order=i)
            i += 1
        if args.dryrun:
            log.info("Dry run mode, will not commit")
        else:
            app.update()

    print("OK")


def choose_func(planner_item):
    tasks = planner_item.item.tasks
    if len(tasks) > 0:
        r = tasks[0]
        planner_item.item.tasks = tasks[1:]
        return r
    else:
        return None


def schedule(app, res, offset=0, tasks_per_day=10):
    """ offset is the position that we should start plan for today's taks. That
        means if today we've finished n tasks, we skip the first n finished
        tasks and start to plan the n+1 task.
    """
    if offset >= tasks_per_day:
        log.warn("offset too large: %d", offset)
        offset = tasks_per_day  # Good job! Award him/her with more tasks!

    j = offset
    for task in res:
        # schedule t for today
        seq = j
        #tp.schedule_for(t.id, j)
        day = int(floor(seq / tasks_per_day))
        minute = seq % tasks_per_day
        date_string = "in {day} days at 22:{minute:02}".format(
            day=day, minute=minute)
        app.update_task(task, date_string=date_string)
        log.info("Task planned at \"%s\". Task: %-20s" % (date_string, task))
        # t: Pytodoist Task
        app.mark_as_planned(task)
        j += 1


def plan(app, args, cfg):
    def adjust_for_completed_tasks(stats):
        total = 0
        done = 0
        # completed tasks are sorted from new to old
        tasks = app.get_completed_tasks()
        now = datetime.now()
        for t in tasks:
            if (now - t.ts_done).total_seconds() > 3 * 24 * 3600:
                # larger than 3 days
                break
            pid = t.pid
            if pid in stats:
                stats[pid] += 1
            else:
                stats[pid] = 1
            total += 1

            if t.done:
                done += 1
        stats['total'] = total
        stats['done'] = done

    projects = app.get_projects()
    project_blacklist = cfg["plan_skip_projects"]
    for p in projects[:]:
        if p.name in project_blacklist:
            log.info("skip project when planning: %s", p.name)
            projects.remove(p)

    planner = PriorityPlanner(cfg, preprocess=adjust_for_completed_tasks)

    n = 0
    res = []
    for t in planner.plan(projects, choose_func):
        res.append(t)
        n += 1
        if n >= args.limit:
            break
    offset = app.num_tasks_completed_today(cfg["timezone"])
    log.debug("Schedule offset: %d" % offset)

    log.debug("Plan result:")
    for item in res:
        log.debug("%s", item)
    # planner.run(projects)
    schedule(app, res, offset=offset, tasks_per_day=args.daily_goal)

    app.clean_up()

    if args.dryrun:
        log.info("Dry run mode, will not commit")
    else:
        app.update()

    print("OK")


def test(app, args, cfg):
    print(args)
    #offset = app.num_tasks_completed_today(cfg["timezone"])
    print(app.user.is_premium)
