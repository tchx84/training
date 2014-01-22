# -*- coding: utf-8 -*-
# Copyright (c) 2013,14 Walter Bender

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# You should have received a copy of the GNU General Public License
# along with this library; if not, write to the Free Software
# Foundation, 51 Franklin Street, Suite 500 Boston, MA 02110-1335 USA

import logging
_logger = logging.getLogger('training-activity-progressbar')

from gi.repository import Gtk

from sugar3.graphics import style

from tasks import SECTIONS

_HEIGHT = 15
_BLACK = style.COLOR_BLACK.get_html()
_WHITE = style.COLOR_WHITE.get_html()
_SIZE = 'medium'


class ProgressBar(Gtk.Grid):

    def __init__(self, name, section, progress_button_data,
                 prev_task_button_cb, next_task_button_cb, progress_button_cb):
        Gtk.Grid.__init__(self)

        self.set_row_spacing(0)  # style.DEFAULT_SPACING)
        self.set_column_spacing(style.DEFAULT_SPACING)
        self.set_border_width(0) # style.DEFAULT_SPACING * 2)

        # FIX ME
        separator = Gtk.SeparatorToolItem()
        separator.props.draw = True
        separator.set_expand(True)
        self.attach(separator, 0, 0, 5, 1)
        separator.show()

        self._prev_grid = Gtk.Grid()
        self._prev_grid.set_row_spacing(0)  # style.DEFAULT_SPACING)
        self._prev_grid.set_column_spacing(style.DEFAULT_SPACING)
        self._prev_grid.set_border_width(0) # style.DEFAULT_SPACING * 2)
        self._prev_grid.set_size_request(-1, _HEIGHT)

        self._progress_button_grid = Gtk.Grid()
        self._progress_button_grid.set_row_spacing(0) # style.DEFAULT_SPACING)
        self._progress_button_grid.set_column_spacing(style.DEFAULT_SPACING)
        self._progress_button_grid.set_border_width(0) # style.DEFAULT_SPACING * 2)
        self._progress_button_grid.set_size_request(-1, _HEIGHT)

        self._next_grid = Gtk.Grid()
        self._next_grid.set_row_spacing(0) # style.DEFAULT_SPACING)
        self._next_grid.set_column_spacing(style.DEFAULT_SPACING)
        self._next_grid.set_border_width(0) # style.DEFAULT_SPACING * 2)
        self._next_grid.set_size_request(-1, _HEIGHT)

        self._progress_buttons = []
        for i, button_data in enumerate(progress_button_data):
            self._progress_buttons.append(Gtk.Button(button_data['label']))
            if 'tooltip' in button_data:
                tooltip = \
'<span background="%s" foreground="%s" size="%s"> %s </span>' \
                    % (_WHITE, _BLACK, _SIZE, button_data['tooltip'])
                self._progress_buttons[i].connect(
                    'clicked', progress_button_cb, i)
                self._progress_buttons[i].set_tooltip_markup(tooltip)
            self._progress_button_grid.attach(
                self._progress_buttons[i], i, 0, 1, 1)
            self._progress_buttons[i].show()
            self._progress_buttons[-1].set_sensitive(False)

        self._section_label = Gtk.Label()
        self._section_label.set_size_request(250, _HEIGHT)
        self._section_label.set_use_markup(True)
        self._section_label.set_justify(Gtk.Justification.LEFT)
        span = '<span foreground="%s" size="%s">' % (_BLACK, _SIZE)
        self._section_label.set_markup(
            span + SECTIONS[section]['name'] + '</span>')
        self.attach(self._section_label, 0, 1, 1, 1)
        self._section_label.show()

        self.prev_task_button = Gtk.Button('<')
        self.prev_task_button.connect('clicked', prev_task_button_cb)
        self._prev_grid.attach(self.prev_task_button, 0, 0, 1, 1)
        self.prev_task_button.show()
        self.prev_task_button.set_sensitive(False)
        self.attach(self._prev_grid, 1, 1, 1, 1)
        self._prev_grid.show()

        self.attach(self._progress_button_grid, 2, 1, 1, 1)
        self._progress_button_grid.show()

        self.next_task_button = Gtk.Button('>')
        self.next_task_button.connect('clicked', next_task_button_cb)
        self._next_grid.attach(self.next_task_button, 0, 0, 1, 1)
        self.next_task_button.show()
        self.next_task_button.set_sensitive(False)
        self.attach(self._next_grid, 3, 1, 1, 1)
        self._next_grid.show()

        self._name_label = Gtk.Label()
        self._name_label.set_size_request(250, _HEIGHT)
        self._name_label.set_use_markup(True)
        self._name_label.set_justify(Gtk.Justification.RIGHT)
        span = '<span foreground="%s" size="%s">' % (_BLACK, _SIZE)
        self._name_label.set_markup(span + name + '</span>')
        self.attach(self._name_label, 4, 1, 1, 1)
        self._name_label.show()

    def set_button_sensitive(self, i, flag=True):
        # _logger.debug('setting button %d to %r' % (i, flag))
        if i < len(self._progress_buttons):
            self._progress_buttons[i].set_sensitive(flag)

    def hide_prev_next_task_buttons(self):
        self.prev_task_button.hide()
        self.next_task_button.hide()

    def show_prev_next_task_buttons(self):
        self.prev_task_button.show()
        self.next_task_button.show()
