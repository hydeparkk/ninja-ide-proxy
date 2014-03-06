# -*- coding: UTF-8 -*-
import os

from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QAction
from PyQt4.QtCore import QSettings

from ninja_ide import resources
from ninja_ide.core import plugin


class Proxy(plugin.Plugin):
    def initialize(self):
        self.menu = self.locator.get_service('menuApp')
        self.proxy_menu_item = QAction('Proxy Settings', self)
        menu_service.add_action(self.proxy_menu_item)
        #lint:disable
        try:
            from urllib.request import urlopen
            from urllib.request import ProxyHandler
            from urllib.request import build_opener
            from urllib.request import install_opener
        except ImportError:
            from urllib2 import urlopen
            from urllib2 import ProxyHandler
            from urllib2 import build_opener
            from urllib2 import install_opener
        #lint:enable

        install_opener(build_opener(ProxyHandler({'http': ''})))

    def finish(self):
        # Shutdown your plugin
        pass

    def get_preferences_widget(self):
        # Return a widget for customize your plugin
        pass

    def load_settings(self):
        qsettings = QSettings(resources.SETTINGS_PATH, QSettings.IniFormat)

class ProxyPreferencesWidget():
    pass