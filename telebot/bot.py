import copy
import functools
from glob import glob
import logging
import importlib
import os
import pkgutil
import sys
import traceback

from emoji import emojize
from telegram.ext import CommandHandler
from telegram.ext import Updater

import telebot.plugins

CURDIR = os.path.abspath(os.path.dirname(__file__))
DIR = functools.partial(os.path.join, CURDIR)
LOG = logging.getLogger(__name__)


def strip_extension(lst):
    return (os.path.splitext(l)[0] for l in lst)


class Bot(object):
    def __init__(self, token):
        self.scheduler = None
        self.updater = Updater(token=token)
        self.dispatcher = self.updater.dispatcher
        self.plugins = {}
        self.plugin_modules = []
        self.init_handlers()

    def init_handlers(self):
        """Init all command handlers"""
        self.init_plugins()
        # Init general command handlers
        start_handler = CommandHandler('start', self.start)
        self.dispatcher.add_handler(start_handler)
        help_handler = CommandHandler('help', self.help)
        self.dispatcher.add_handler(help_handler)
        # Init additional plugins handlers
        for plugin in self.plugins.keys():
            _handler = CommandHandler(plugin, self.plugins[plugin]['handler'])
            self.dispatcher.add_handler(_handler)

    def _get_commands(self):
        commands = []
        for name, helper in self.plugins.items():
            command = '/' + name
            whatis = helper['whatis']
            commands.append([command, whatis])
        return commands

    def run(self):
        self.updater.start_polling()
        return

    def start(self, bot, update):
        bot.send_message(chat_id=update.message.chat_id,
                         text='Hallo! I\'m Telebot, please type /help for '
                              'more info')

    def help(self, bot, update):
        # Fancy icon
        icon = emojize(":information_source:", use_aliases=True)
        commands = self._get_commands()
        command_names = [cmd[0].strip('/') for cmd in commands]

        text = 'Please type: /help <command> with <command> is optional.'
        user_input = update.message.text.split(' ')
        if len(user_input) == 1:
            text = icon + ' The following commands are available:\n'

            for command in commands:
                text += command[0] + '-' + command[1] + '\n'
        elif len(user_input) == 2 and user_input[1] in command_names:
            text = icon + ' ' + self.plugins[user_input[1]]['usage']

        bot.send_message(chat_id=update.message.chat_id, text=text)

    def init_plugins(self):
        # Default
        plugindir = DIR('plugins')
        LOG.debug('Plugindir: {}' . format(plugindir))

        for _, name, _ in pkgutil.iter_modules(telebot.plugins.__path__):
            try:
                LOG.debug('Plugin: {}' . format(name))
                module = importlib.import_module('telebot.plugins.' + name)
                module_name = module.__name__.split('.')[-1]
                _info = {
                    'whatis': 'Unknow command',
                    'usage': 'Unknow usage',
                    'handler': getattr(module, 'handle')
                }

                LOG.info(_info)

                if module.__doc__:
                    _info['whatis'] = module.__doc__.split('\n')[0]
                    _info['usage'] = module.__doc__
                self.plugins[module_name] = _info
            except:
                LOG.warning('Import failed on module {}, module not loaded!' .
                            format(name))
                LOG.warning('{}' . format(sys.exc_info()[0]))
                LOG.warning('{}' . format(traceback.format_exc()))
