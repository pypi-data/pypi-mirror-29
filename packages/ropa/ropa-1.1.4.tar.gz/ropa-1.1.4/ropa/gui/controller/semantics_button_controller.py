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

from button_controller import ButtonController


class SemanticsButtonController(ButtonController):
    def __init__(self, app, widget):
        super(SemanticsButtonController, self).__init__(app, widget)

        self._bind_clicked(self.filter)
        self.widget.setToolTip(
            "Search for gadgets using Ropper's semantic searching function")

    def filter(self):
        input_box = self.app.filter_input
        lwc = self.app.search_list
        blocks = self.search_service.process_query('semantic',
                                                   input_box.get_text())
        lwc.set_blocks(blocks)
