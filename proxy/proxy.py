# -*- coding: UTF-8 -*-
import os
import base64

from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QAction
from PyQt4.QtCore import QSettings

from ninja_ide import resources
from ninja_ide.core import plugin


class Proxy(plugin.Plugin):
    def initialize(self):
        self.menu = self.locator.get_service('menuApp')
        self.proxy_menu_item = QAction('Proxy Settings', self)
        self.menu.add_action(self.proxy_menu_item)
        self.preferences_widget = ProxyPreferencesWidget()
        self.preferences_widget.save()
        self.preferences = self.preferences_widget.load_settings()

        #lint:disable
        try:
            from urllib.request import ProxyHandler
            from urllib.request import build_opener
            from urllib.request import install_opener
        except ImportError:
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


class ProxyPreferencesWidget():
    def __init__(self):
        pass

    def save(self):
        qsettings = QSettings(resources.SETTINGS_PATH, QSettings.IniFormat)
        qsettings.beginGroup('proxy')
        qsettings.setValue('enabled', True)
        qsettings.setValue('server', '')
        qsettings.setValue('login', '')
        qsettings.setValue('password', base64.b64encode('test'))
        qsettings.endGroup()

    def load_settings(self):
        qsettings = QSettings(resources.SETTINGS_PATH, QSettings.IniFormat)
        self.proxy_enabled = qsettings.value('proxy/enabled', True, type=bool)
        self.proxy_server = qsettings.value('proxy/server', '', type='QString')
        self.proxy_login = qsettings.value('proxy/login', '', type='QString')
        self.proxy_password = base64.b64decode(qsettings.value('proxy/password', '', type='QString'))
