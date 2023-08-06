import os

import coloredlogs

import app.arguments as arguments
import app.taski as taski


def main():
    """
    Parse arguments and dispatch to different functions to handle
    different use cases
    """
    args = arguments.parse()
    FORMAT = "%(asctime)-15s %(levelname)-6s %(message)s"
    os.environ['COLOREDLOGS_LOG_FORMAT'] = FORMAT
    if args.verbose:
        coloredlogs.install(level='DEBUG')
    else:
        coloredlogs.install(level='INFO')

    if hasattr(args, "quick_func"):
        args.quick_func(args)
    elif hasattr(args, "func"):
        cfg = taski.get_config(args)
        app = taski.get_app(cfg)
        args.func(app, args, cfg)
