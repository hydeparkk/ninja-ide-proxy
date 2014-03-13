# -*- coding: UTF-8 -*-
import os
import base64

from PyQt4.QtGui import QAction
from PyQt4.QtGui import QFormLayout
from PyQt4.QtGui import QLineEdit
from PyQt4.QtGui import QDialogButtonBox
from PyQt4.QtGui import QCheckBox
from PyQt4.QtGui import QLabel
from PyQt4.QtGui import QDialog
from PyQt4.QtGui import QIcon
from PyQt4.QtGui import QPushButton
from PyQt4.QtGui import QHBoxLayout
from PyQt4.QtCore import Qt
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
        QObject.connect(self.proxy_menu_item, SIGNAL('triggered()'), self.open_preferences)

        self.preferences = self.load_settings()
        self.set_proxy()

    def finish(self):
        # Shutdown your plugin
        pass

    def open_preferences(self):
        preferences_widget = ProxyPreferencesWidget(parent=None)
        preferences_widget.set_values(self.preferences)
        ret = preferences_widget.exec_()
        if ret == 1:
            self.preferences = self.load_settings()
            self.set_proxy()

    def set_proxy(self):
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

        if self.preferences['proxy_enabled']:
            if self.preferences['proxy_login'] == '' and self.preferences['proxy_password'] == '':
                install_opener(build_opener(ProxyHandler({'http': self.preferences['proxy_server']})))
            else:
                proxyUrl = self.preferences['proxy_login'] + ':' + self.preferences['proxy_password'] + '@' + self.preferences['proxy_server']
                install_opener(build_opener(ProxyHandler({'http': proxyUrl})))
        else:
            install_opener(build_opener(ProxyHandler({'http': ''})))

    def load_settings(self):
        prefs = {}
        qsettings = QSettings(resources.SETTINGS_PATH, QSettings.IniFormat)
        prefs['proxy_enabled'] = qsettings.value('proxy/enabled', False, type=bool)
        prefs['proxy_server'] = qsettings.value('proxy/server', '', type='QString')
        prefs['proxy_login'] = qsettings.value('proxy/login', '', type='QString')
        prefs['proxy_password'] = base64.b64decode(qsettings.value('proxy/password', '', type='QString'))
        return prefs

    def load_settins_from_env(self):
        prefs = {}
        env_proxy = os.environ.get('HTTP_PROXY')
        if env_proxy is not None:
            prefs['proxy_enabled'] = True
            if os.environ.get('HTTP_PROXY_USER') is not None and os.environ.get('HTTP_PASS') is not None:
                prefs['proxy_server'] = env_proxy[7:]
                prefs['proxy_login'] = os.environ.get('HTTP_PROXY_USER')
                prefs['proxy_password'] = os.environ.get('HTTP_PASS')
            else:
                if env_proxy[:7] == 'http://' and len(env_proxy.split('@')) == 2:
                    prefs['proxy_server'] = env_proxy[7:].split('@')[1]
                    prefs['proxy_login'], prefs['proxy_password'] = env_proxy[7:].split('@')[0].split(':')
                else:
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
        self.proxyEnable.stateChanged.connect(self.enable_edit)
        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.proxyEnable)
        self.envProxyEnable = QCheckBox(self)
        self.envProxyEnable.setObjectName('envProxyEnable')
        #self.envProxyEnable.stateChanged.connect(self.enable_edit)
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.envProxyEnable)
        self.proxyServer = QLineEdit(self)
        self.proxyServer.setObjectName('proxyServer')
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.proxyServer)
        self.proxyLogin = QLineEdit(self)
        self.proxyLogin.setObjectName('proxyLogin')
        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.proxyLogin)
        #self.proxyPass = QLineEdit(self)
        plug_path = os.path.abspath(__file__)
        plug_path = os.path.dirname(plug_path)
        self.proxyPass = ButtonInLineEdit(self, plug_path + '/eye.svg')
        self.proxyPass.setObjectName('proxyPass')
        self.proxyPass.setEchoMode(QLineEdit.Password)
        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.proxyPass)
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.buttonBox.setObjectName('buttonBox')
        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.buttonBox)
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
        QObject.connect(self.proxyPass.Button, SIGNAL('pressed()'), lambda: self.proxyPass.setEchoMode(QLineEdit.Normal))
        QObject.connect(self.proxyPass.Button, SIGNAL('released()'), lambda: self.proxyPass.setEchoMode(QLineEdit.Password))
        QMetaObject.connectSlotsByName(self)

    def show_pass(self):
        self.proxyPass.setEchoMode(QLineEdit.Normal)

    def enable_edit(self):
        if not self.proxyEnable.isChecked():
            self.proxyServer.setEnabled(False)
            self.proxyLogin.setEnabled(False)
            self.proxyPass.setEnabled(False)
        else:
            self.proxyServer.setEnabled(True)
            self.proxyLogin.setEnabled(True)
            self.proxyPass.setEnabled(True)

    def set_values(self, preferences):
        self.proxyEnable.setChecked(preferences['proxy_enabled'])
        self.proxyServer.setText(preferences['proxy_server'])
        self.proxyLogin.setText(preferences['proxy_login'])
        self.proxyPass.setText(preferences['proxy_password'])
        self.enable_edit()

    def save_settings(self):
        qsettings = QSettings(resources.SETTINGS_PATH, QSettings.IniFormat)
        qsettings.beginGroup('proxy')
        qsettings.setValue('enabled', self.proxyEnable.isChecked())
        qsettings.setValue('server', self.proxyServer.text())
        qsettings.setValue('login', self.proxyLogin.text())
        qsettings.setValue('password', base64.b64encode(self.proxyPass.text()))
        qsettings.endGroup()
        self.accept()


class ButtonInLineEdit(QLineEdit):
    def __init__(self, parent=None, icon=None):
        QLineEdit.__init__(self, parent)

        self.Button = QPushButton(self)
        self.Button.setCursor(Qt.PointingHandCursor)
        self.Button.setFocusPolicy(Qt.NoFocus)
        self.Button.setIcon(QIcon(icon))
        #self.Button.setStyleSheet('background: transparent; border: none;')
        layout = QHBoxLayout(self)
        layout.addWidget(self.Button, 0, Qt.AlignRight)

        layout.setSpacing(0)
        layout.setMargin(1)
