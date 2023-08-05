#!/usr/bin/env python
# -*- coding: utf-8 -*-

##  Photini - a simple photo metadata editor.
##  http://github.com/jim-easterbrook/Photini
##  Copyright (C) 2012-18  Jim Easterbrook  jim@jim-easterbrook.me.uk
##
##  This program is free software: you can redistribute it and/or
##  modify it under the terms of the GNU General Public License as
##  published by the Free Software Foundation, either version 3 of the
##  License, or (at your option) any later version.
##
##  This program is distributed in the hope that it will be useful,
##  but WITHOUT ANY WARRANTY; without even the implied warranty of
##  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
##  General Public License for more details.
##
##  You should have received a copy of the GNU General Public License
##  along with this program.  If not, see
##  <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals

import logging
import os
import site
import sys

logger = logging.getLogger(__name__)

# avoid "dll Hell" on Windows by getting PyEnchant to use GObject's
# copy of libenchant and associated libraries
if sys.platform == 'win32':
    # disable PyEnchant's forced use of its bundled DLLs
    sys.platform = 'win32x'
    # add gnome DLLs to PATH
    for name in site.getsitepackages():
        gnome_path = os.path.join(name, 'gnome')
        if os.path.isdir(gnome_path) and gnome_path not in os.environ['PATH']:
            os.environ['PATH'] = gnome_path + ';' + os.environ['PATH']
            break

try:
    import enchant
    enchant_version = 'enchant {}'.format(enchant.__version__)
except ImportError:
    enchant = None
    enchant_version = None

if sys.platform == 'win32x':
    # reset sys.platform
    sys.platform = 'win32'
    # using PyGObject's copy of libenchant means it won't find the
    # dictionaries installed with PyEnchant
    if enchant:
        for name in site.getsitepackages():
            dict_path = os.path.join(
                name, 'enchant', 'share', 'enchant', 'myspell')
            if os.path.isdir(dict_path):
                enchant.set_param('enchant.myspell.dictionary.path', dict_path)
                break

from photini.pyqt import Qt, QtCore, QtGui, QtWidgets

class SpellCheck(QtCore.QObject):
    new_dict = QtCore.pyqtSignal()

    def __init__(self, *arg, **kw):
        super(SpellCheck, self).__init__(*arg, **kw)
        self.config_store = QtWidgets.QApplication.instance().config_store
        self.enable(eval(self.config_store.get('spelling', 'enabled', 'True')))
        self.set_dict(self.config_store.get('spelling', 'language'))

    @staticmethod
    def available_languages():
        if not enchant:
            return []
        result = enchant.list_languages()
        result.sort()
        return result

    def current_language(self):
        if self.dict:
            return self.dict.tag
        return ''

    @QtCore.pyqtSlot(bool)
    def enable(self, enabled):
        self.enabled = bool(enchant) and enabled
        self.config_store.set('spelling', 'enabled', str(self.enabled))
        self.new_dict.emit()

    @QtCore.pyqtSlot(QtWidgets.QAction)
    def set_language(self, action):
        self.set_dict(action.text().replace('&', ''))

    def set_dict(self, tag):
        if tag:
            logger.debug('Setting dictionary %s', tag)
        if tag and enchant and enchant.dict_exists(tag):
            self.dict = enchant.Dict(tag)
        else:
            if tag:
                logger.warning('Failed to set dictionary %s', tag)
            self.dict = None
        self.config_store.set('spelling', 'language', self.current_language())
        self.new_dict.emit()
