#!/usr/bin/env python

from __future__ import print_function
from pydoc import locate
from pkg_resources import resource_filename
from pathlib import Path
from collections import OrderedDict
import argparse
import getpass
import logging
import os
import time
import schedule
import threading
import yaml
import shutil
import keyring


class CloudToken(object):
    def __init__(self):
        self.config = None  # Initialise config variable.


    @staticmethod
    def filter_classes(cls_obj):
        if cls_obj.__name__ == 'CloudTokenPlugin':
            return True

        return False

    def load_plugins(self):
        plugins = OrderedDict([('pre_auth', list()), ('auth', list()), ('post_auth', list())])

        if self.config:
            for plugin_type in ['pre_auth', 'auth', 'post_auth']:
                if self.config['plugins'][plugin_type]:
                    for plugin in self.config['plugins'][plugin_type]:
                        logging.debug("Loading plugin {0}.".format(plugin))
                        obj = locate('cloudtoken_plugin.{0}.Plugin'.format(plugin))
                        if obj is None:
                            print("Unable to load plugin: {0}".format(plugin))
                            print("Exiting.")
                            exit(1)
                        try:
                            plugins[plugin_type].append(obj(self.config))
                        except Exception:
                            raise Exception("Problem loading plugin: {plugin}".format(plugin=plugin))

        return plugins

    def default_parser_args(self, plugins=None, add_help=True):
        """
        Define an ArgumentParser and set default command line options.

        returns parser.parse_args() list.
        """
        all_plugin_objects = list()
        defaults = dict()

        if self.config:
            defaults = self.config.get('defaults', dict())
            if plugins:
                for plugin in self.iterate_plugins(plugins):
                    all_plugin_objects.append(plugin)

        parser = argparse.ArgumentParser(prog="cloudtoken",
                                         description="Command line utility for authenticating with public clouds.",
                                         conflict_handler="resolve",
                                         parents=[plugin.arguments(defaults) for plugin in all_plugin_objects],
                                         add_help=add_help,
                                         allow_abbrev=False)
        parser.add_argument("-u",
                            "--username",
                            help="Your username",
                            default="{0}".format(defaults.get('username', getpass.getuser())))
        parser.add_argument("-p",
                            "--password",
                            help="Your password.",
                            default=defaults.get('password', None))
        parser.add_argument("--password-file",
                            help="File containing your password.",
                            type=argparse.FileType('r'),
                            default=defaults.get('password-file', None))
        parser.add_argument("-U",
                            "--unset",
                            action='store_true',
                            help="Remove references to current credentials from your system.")
        parser.add_argument("-q",
                            "--quiet",
                            action='store_true',
                            default=defaults.get('quiet', False),
                            help="Suppress most output.")
        parser.add_argument("--refresh-interval",
                            default=defaults.get('refresh-interval', (60*45)),
                            type=int,
                            help="How often do we refresh the token (in seconds) if --deamon (-d) is specified.")
        parser.add_argument("--debug",
                            dest='debug',
                            action='store_true',
                            default=defaults.get('debug', False),
                            help="Print debug information.")
        parser.add_argument("-d",
                            "--daemon",
                            dest='daemon',
                            action='store_true',
                            default=defaults.get('daemon', False),
                            help="Run a fake AWS metadata proxy.")
        parser.add_argument("-i",
                            "--init",
                            dest='init',
                            action='store_true',
                            help='Initialise ~/config/.cloudtoken directory and populate with skeleton files.')
        parser.add_argument("--cloudtoken-dir",
                            dest='cloudtoken_dir',
                            default="{0}/.config/cloudtoken".format(str(Path.home())),
                            type=str,
                            help='Cloudtoken directory.')
        parser.add_argument("--config-file",
                            dest='config_file',
                            default="{0}/.config/cloudtoken/config.yaml".format(str(Path.home())),
                            type=str,
                            help='Configuration file.')

        return parser

    @staticmethod
    def unset(plugin, args):
        logging.debug("Running {0}.unset()".format(plugin))
        try:
            plugin.unset(args)
        except TypeError as e:
            print("Exception when executing unset() on plugin {0}: {1}".format(plugin, e))
            exit(1)

    def metadata_proxy(self, args):
        from cloudtoken.proxy import Proxy
        proxy = Proxy(self.config, args)
        proxy.run()

    def create_cloudtoken_directory(self, directory):
        if not os.path.exists(directory):
            os.makedirs(directory)

    def copy_skeleton_config_files(self, directory):
        basedir = os.path.dirname(resource_filename(__name__, ""))
        for filename in ['config.yaml', 'proxy.yaml']:
            source = basedir + "/share/cloudtoken/configs/{0}".format(filename)
            logging.debug("SOURCE: {0}".format(source))
            dest = "{dir}/{file}".format(dir=directory, file=filename)

            if os.path.isfile(dest) is False:
                shutil.copyfile(source, dest)
            else:
                print("{0} already exists. Ignoring.".format(dest))

    @staticmethod
    def run_plugin(plugin, args, data, flags):
        logging.debug("Running plugin: {0}".format(plugin))
        data = plugin.execute(data, args, flags)
        logging.debug("Data Returned From {0}: {1}".format(plugin, data))

        if not isinstance(data, list):
            print("Plugin {0} did not return valid data. Must return list, returned: {1}".format(plugin, type(data)))
            exit(1)

        return data

    def scheduler_plugin_runner(self, plugins, args, data, flags):
        for plugin in plugins:
                data = self.run_plugin(plugin=plugin, args=args, data=data, flags=flags)

    def init(self, directory):
        print("Creating {0} directory.".format(directory))
        self.create_cloudtoken_directory(directory)
        print("Populating {0} with skeleton configuration files.".format(directory))
        self.copy_skeleton_config_files(directory)
        print("Initialisation complete.")
        print("Please see the documentation for instructions on completing shell integration.")

    @staticmethod
    def set_logging_levels(args):
        logger = logging.getLogger()
        handler = logging.StreamHandler()
        logger.addHandler(handler)
        logger.setLevel(logging.WARNING)
        if args.debug:
            logger.setLevel(logging.DEBUG)

    @staticmethod
    def iterate_plugins(plugins):
        """
        Generator to iterate over the loaded plugins.
        :param plugins: dict of plugins as generated by load_plugins().
        :return: plugin
        """
        for category in plugins.keys():
            for plugin in plugins.get(category, []):
                yield plugin

    @staticmethod
    def save_password(username, password):
        try:
            keyring.set_password("cloudtoken", username, password)
            print("Saved password.")
            return True
        except RuntimeError:
            print("No supported keyring backend found - unable to store password.")
            return False

    def main(self):
        # Load argparse initially so we can capture --config and load an alternate config file if required.
        # use parse_known_args() so it ignores unknown arguments.
        parser = self.default_parser_args(add_help=False)
        args = parser.parse_known_args()[0]

        if args.init:
            self.init(args.cloudtoken_dir)
            exit(1)

        try:
            with open(args.config_file) as fh:
                self.config = yaml.load(fh.read())
        except IOError:
            print("Unable to load config file: {0}".format(args.config_file))
            parser.print_help()
            exit(1)

        self.config['config_dir'] = args.cloudtoken_dir

        plugins = self.load_plugins()
        if len(plugins['auth']) == 0:
            print("No auth plugins configured. Exiting.")
            exit(1)

        # Load argparse for realz.
        parser = self.default_parser_args(plugins)
        args = parser.parse_args()

        # Password handling.
        if args.password_file:
            args.password = args.password_file.read()

        if args.password:
            self.save_password(args.username, args.password)
        elif not args.password:
            args.password = keyring.get_password("cloudtoken", args.username)
            if args.password is None:
                args.password = getpass.getpass("Password for {0}:".format(args.username))
                self.save_password(args.username, args.password)

        self.set_logging_levels(args)

        if args.unset:
            for plugin in self.iterate_plugins(plugins):
                    self.unset(plugin, args)
            exit(0)

        # Run the plugins.
        data = list()
        for plugin in self.iterate_plugins(plugins):
            data = self.run_plugin(plugin=plugin, args=args, data=data, flags={})

        # Metadata proxy.
        try:
            if args.daemon:
                t = threading.Thread(target=self.metadata_proxy, kwargs={'args': args})
                t.daemon = True
                t.start()

                scheduled_plugins = plugins['auth'] + plugins['post_auth']
                schedule.every(args.refresh_interval).seconds.do(self.scheduler_plugin_runner,
                                                                 plugins=scheduled_plugins,
                                                                 args=args,
                                                                 data=data,
                                                                 flags={'daemon_mode': True})

                proxy_start_msg = 'Metadata proxy now available on http://169.254.169.254'
                print(proxy_start_msg)
                print('-' * len(proxy_start_msg))

                while True:
                    schedule.run_pending()
                    time.sleep(1)
        except KeyboardInterrupt:
            exit(0)


if __name__ == '__main__':
    try:
        cloudtoken = CloudToken()
        cloudtoken.main()
    except KeyboardInterrupt:
        pass
    except Exception:
        raise
