# ropa
# Copyright (C) 2017-2018 orppra

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from list_widget_controller import ListWidgetController
from ropa.ui import HTMLDelegate
from PyQt4 import QtGui as qg


class SearchListController(ListWidgetController):
    def __init__(self, app, widget):
        super(SearchListController, self).__init__(app, widget)
        self.widget.setDragEnabled(True)
        self.widget.setAcceptDrops(False)
        self.widget.setDropIndicatorShown(False)
        self.widget.setVerticalScrollMode(
            qg.QAbstractItemView.ScrollPerPixel)
        self.widget.setItemDelegate(
            HTMLDelegate(self.widget))
