import logging
import importlib
import os
import pkgutil
import sys
import traceback

from telegram.ext import CommandHandler
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import Updater

import telebot.plugins
from telebot import emojies

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
            if plugin == 'remind':
                _handler = CommandHandler(plugin,
                                          self.plugins[plugin]['handler'],
                                          pass_args=True,
                                          pass_job_queue=True,
                                          pass_chat_data=True)

            self.dispatcher.add_handler(_handler)
        file_handler = MessageHandler(filters=Filters.document,
                                      callback=self.get_config_file)
        self.dispatcher.add_handler(file_handler)

    def get_config_file(self, bot, update):
        """Handle config file upload. Stackalytics plugin need this!"""
        if not update.message.document:
            return
        else:
            file_id = update.message.document.file_id
            config_file = bot.get_file(file_id=file_id)
            config_file.download(custom_path='/tmp/stackalyticsconfig.json')

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
        commands = self._get_commands()
        command_names = [cmd[0].strip('/') for cmd in commands]

        text = 'Please type: /help <command> with <command> is optional.'
        user_input = update.message.text.split(' ')
        if len(user_input) == 1:
            text = emojies.information_source + \
                ' The following commands are available:\n'

            for command in commands:
                text += command[0] + '-' + command[1] + '\n'
        elif len(user_input) == 2 and user_input[1] in command_names:
            text = emojies.information_source + ' ' + \
                self.plugins[user_input[1]]['usage']

        bot.send_message(chat_id=update.message.chat_id, text=text)

    def init_plugins(self):
        for _, name, _ in pkgutil.iter_modules(telebot.plugins.__path__):
            try:
                LOG.debug('Plugin: {}' . format(name))
                module = importlib.import_module('telebot.plugins.' + name)
                module_name = module.__name__.split('.')[-1]
                _info = {
                    'whatis': 'Unknown command',
                    'usage': 'Unknown usage',
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
