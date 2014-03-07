# -*- coding: UTF-8 -*-
import os
import base64

from PyQt4.QtGui import QAction
from PyQt4.QtGui import QFormLayout
from PyQt4.QtGui import QLineEdit
from PyQt4.QtGui import QDialogButtonBox
from PyQt4.QtGui import QCheckBox
from PyQt4.QtGui import QLabel
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QDialog
from PyQt4.QtCore import QSettings
from PyQt4.QtCore import QObject
from PyQt4.QtCore import QSize
from PyQt4.QtCore import QMetaObject
from PyQt4.QtCore import SIGNAL

from ninja_ide import resources
from ninja_ide.core import plugin


class Proxy(plugin.Plugin):
    def initialize(self):
        self.menu = self.locator.get_service('menuApp')
        self.proxy_menu_item = QAction('Proxy Settings', self)
        self.menu.add_action(self.proxy_menu_item)
        self.preferences_widget = ProxyPreferencesWidget(parent=None)
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
        QObject.connect(self.proxy_menu_item, SIGNAL('clicked()'), self.preferences_widget.show)

    def finish(self):
        # Shutdown your plugin
        pass

    def get_preferences_widget(self):
        # Return a widget for customize your plugin
        pass


class ProxyPreferencesWidget(QDialog):
    def __init__(self, parent=None):
        super(ProxyPreferencesWidget, self).__init__(parent, Qt.Dialog)
        self.setObjectName('Dialog')
        self.resize(325, 142)
        self.setMinimumSize(QSize(325, 142))
        self.setMaximumSize(QSize(325, 142))
        self.formLayout = QFormLayout(self)
        self.formLayout.setObjectName('formLayout')
        self.proxyEnable = QCheckBox(self)
        self.proxyEnable.setObjectName('proxyEnable')
        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.proxyEnable)
        self.proxyServer = QLineEdit(self)
        self.proxyServer.setObjectName('proxyServer')
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.proxyServer)
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.buttonBox.setObjectName('buttonBox')
        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.buttonBox)
        self.proxyLogin = QLineEdit(self)
        self.proxyLogin.setObjectName('proxyLogin')
        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.proxyLogin)
        self.proxyPass = QLineEdit(self)
        self.proxyPass.setObjectName('proxyPass')
        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.proxyPass)
        self.label = QLabel(self)
        self.label.setObjectName('label')
        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label)
        self.label_2 = QLabel(self)
        self.label_2.setObjectName('label_2')
        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_2)
        self.label_3 = QLabel(self)
        self.label_3.setObjectName('label_3')
        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label_3)

        self.setWindowTitle('Proxy preferences')
        self.proxyEnable.setText('Enable Proxy')
        self.label.setText('Proxy server:port')
        self.label_2.setText('Login')
        self.label_3.setText('Password')

        QObject.connect(self.buttonBox, SIGNAL('accepted()'), self.save_settings)
        QObject.connect(self.buttonBox, SIGNAL('rejected()'), self.reject)
        QMetaObject.connectSlotsByName(self)

    def show(self):
        pass

    def save_settings(self):
        qsettings = QSettings(resources.SETTINGS_PATH, QSettings.IniFormat)
        qsettings.beginGroup('proxy')
        qsettings.setValue('enabled', True)
        qsettings.setValue('server', '')
        qsettings.setValue('login', '')
        qsettings.setValue('password', base64.b64encode('test'))
        qsettings.endGroup()
        self.accept

    def load_settings(self):
        qsettings = QSettings(resources.SETTINGS_PATH, QSettings.IniFormat)
        self.proxy_enabled = qsettings.value('proxy/enabled', True, type=bool)
        self.proxy_server = qsettings.value('proxy/server', '', type='QString')
        self.proxy_login = qsettings.value('proxy/login', '', type='QString')
        self.proxy_password = base64.b64decode(qsettings.value('proxy/password', '', type='QString'))
