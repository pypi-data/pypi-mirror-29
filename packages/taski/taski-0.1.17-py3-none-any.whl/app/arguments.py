
# -*- coding: utf-8 -*-

import os
import sys
import six

import argparse

import app
import app.taski as taski


def check_positive_int(val):
    """Make sure input argument is an positive integer"""
    ival = int(val)
    if ival <= 0:
        raise argparse.ArgumentTypeError("%s is not a positive integer" % val)
    return ival


def str2unicode(val):
    """
    Python2 will set val to type `bytes` while Python3 will set val to
    unicode. So we need to convert bytes to unicode in Python2.
    https://stackoverflow.com/questions/22947181/dont-argparse-read-unicode-from-commandline
    """
    if six.PY2:
        return val.decode(sys.getfilesystemencoding())

    return val


def parse(cmd=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', help="config file path")
    parser.set_defaults(config=os.path.expanduser("~") + "/.taski.yaml")

    parser.add_argument('-d', '--dryrun', help="dryrun", action='store_true')
    parser.add_argument('-v', '--verbose',
                        help="enable debugging", action='store_true')

    subparsers = parser.add_subparsers(help='available commands')

    plan_parser = subparsers.add_parser('plan', help='plan tasks')
    plan_parser.add_argument('-v', '--verbose',
                        help="enable debugging", action='store_true')
    plan_parser.add_argument('-l', '--limit',
                             help='limit number of tasks to plan',
                             type=check_positive_int, default=30)
    plan_parser.add_argument('-n', '--daily-goal',
                             help='number of tasks scheduled per day',
                             type=check_positive_int, default=10)
    plan_parser.set_defaults(func=taski.plan)

    rank_parser = subparsers.add_parser('rank', help='rank tasks')
    rank_parser.add_argument('-v', '--verbose',
                        help="enable debugging", action='store_true')
    rank_parser.add_argument('-p', '--project', help='project name',
                             type=str2unicode)
    rank_parser.add_argument('-t', '--tui', help='Use terminal UI for ranking',
                             default=False, action='store_true')
    rank_parser.set_defaults(func=taski.rank)

    show_parser = subparsers.add_parser('show', help='show things')
    show_parser.add_argument('show_cmd', help='show things',
                             choices=["api_token", "stats", "config", "old_tasks", "completed_tasks"])
    show_parser.add_argument(
        '--since', help='show completed task since this date. Format "2007-4-29T10:13"')
    show_parser.add_argument(
        '--until', help='show completed task until this date. Format "2007-4-29T10:13"')
    show_parser.set_defaults(since=None)
    show_parser.set_defaults(until=None)
    show_parser.set_defaults(func=taski.show)

    version_parser = subparsers.add_parser(
        'version', help='print version number')
    version_parser.set_defaults(
        quick_func=lambda args: sys.stdout.write(app.VERSION + "\n"))
    test_parser = subparsers.add_parser('test', help="¯\_(ツ)_/¯")
    test_parser.set_defaults(func=taski.test)

    if cmd:
        args = parser.parse_args(cmd)
    else:
        args = parser.parse_args()

    return args
