"""
Copyright 2007, 2008, 2009 Free Software Foundation, Inc.
This file is part of GNU Radio

GNU Radio Companion is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

GNU Radio Companion is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA
"""

from __future__ import absolute_import
from gi.repository import Gtk, Gdk, GObject, Pango

from . import Actions, Utils, Constants
from .Dialogs import SimpleTextDisplay
import six


class PropsDialog(Gtk.Dialog):
    """
    A dialog to set block parameters, view errors, and view documentation.
    """

    def __init__(self, parent, block):
        """
        Properties dialog constructor.

        Args:%
            block: a block instance
        """

        Gtk.Dialog.__init__(
            self,
            title='Properties: ' + block.get_name(),
            transient_for=parent,
            modal=True,
        )
        self.add_buttons(
            Gtk.STOCK_OK, Gtk.ResponseType.ACCEPT,
            Gtk.STOCK_CANCEL, Gtk.ResponseType.REJECT,
            Gtk.STOCK_APPLY, Gtk.ResponseType.APPLY,
        )
        self.set_response_sensitive(Gtk.ResponseType.APPLY, False)
        self.set_size_request(Constants.MIN_DIALOG_WIDTH, Constants.MIN_DIALOG_HEIGHT)

        self._block = block
        self._hash = 0

        vpaned = Gtk.VPaned()
        self.vbox.pack_start(vpaned, True, True, 0)

        # Notebook to hold param boxes
        notebook = Gtk.Notebook()
        notebook.set_show_border(False)
        notebook.set_scrollable(True)  # scroll arrows for page tabs
        notebook.set_tab_pos(Gtk.PositionType.TOP)
        vpaned.pack1(notebook, True)

        # Params boxes for block parameters
        self._params_boxes = list()
        for tab in block.get_param_tab_labels():
            label = Gtk.Label()
            vbox = Gtk.VBox()
            scroll_box = Gtk.ScrolledWindow()
            scroll_box.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
            scroll_box.add_with_viewport(vbox)
            notebook.append_page(scroll_box, label)
            self._params_boxes.append((tab, label, vbox))

        # Docs for the block
        self._docs_text_display = doc_view = SimpleTextDisplay()
        doc_view.get_buffer().create_tag('b', weight=Pango.Weight.BOLD)
        self._docs_box = Gtk.ScrolledWindow()
        self._docs_box.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self._docs_box.add_with_viewport(self._docs_text_display)
        notebook.append_page(self._docs_box, Gtk.Label(label="Documentation"))

        # Generated code for the block
        if Actions.TOGGLE_SHOW_CODE_PREVIEW_TAB.get_active():
            self._code_text_display = code_view = SimpleTextDisplay()
            code_view.set_wrap_mode(Gtk.WrapMode.NONE)
            code_view.get_buffer().create_tag('b', weight=Pango.Weight.BOLD)
            code_view.set_monospace(True)
            # todo: set font size in non-deprecated way
            # code_view.override_font(Pango.FontDescription('monospace %d' % Constants.FONT_SIZE))
            code_box = Gtk.ScrolledWindow()
            code_box.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
            code_box.add_with_viewport(self._code_text_display)
            notebook.append_page(code_box, Gtk.Label(label="Generated Code"))
        else:
            self._code_text_display = None

        # Error Messages for the block
        self._error_messages_text_display = SimpleTextDisplay()
        self._error_box = Gtk.ScrolledWindow()
        self._error_box.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self._error_box.add_with_viewport(self._error_messages_text_display)
        vpaned.pack2(self._error_box)
        vpaned.set_position(int(0.65 * Constants.MIN_DIALOG_HEIGHT))

        # Connect events
        self.connect('key-press-event', self._handle_key_press)
        self.connect('show', self.update_gui)
        self.connect('response', self._handle_response)
        self.show_all()  # show all (performs initial gui update)

    def _params_changed(self):
        """
        Have the params in this dialog changed?
        Ex: Added, removed, type change, hide change...
        To the props dialog, the hide setting of 'none' and 'part' are identical.
        Therefore, the props dialog only cares if the hide setting is/not 'all'.
        Make a hash that uniquely represents the params' state.

        Returns:
            true if changed
        """
        old_hash = self._hash
        new_hash = self._hash = hash(tuple(
            (hash(param), param.get_name(), param.get_type(), param.get_hide() == 'all',)
            for param in self._block.get_params()
        ))
        return new_hash != old_hash

    def _handle_changed(self, *args):
        """
        A change occurred within a param:
        Rewrite/validate the block and update the gui.
        """
        self._block.rewrite()
        self._block.validate()
        self.update_gui()

    def _activate_apply(self, *args):
        self.set_response_sensitive(Gtk.ResponseType.APPLY, True)

    def update_gui(self, widget=None, force=False):
        """
        Repopulate the parameters boxes (if changed).
        Update all the input parameters.
        Update the error messages box.
        Hide the box if there are no errors.
        Update the documentation block.
        Hide the box if there are no docs.
        """
        if force or self._params_changed():
            # hide params box before changing
            for tab, label, vbox in self._params_boxes:
                vbox.hide()
                # empty the params box
                for child in vbox.get_children():
                    vbox.remove(child)
                    # child.destroy()   # disabled because it throw errors...
                # repopulate the params box
                box_all_valid = True
                for param in [p for p in self._block.get_params() if p.get_tab_label() == tab]:
                    # fixme: why do we even rebuild instead of really hiding params?
                    if param.get_hide() == 'all':
                        continue
                    box_all_valid = box_all_valid and param.is_valid()

                    input_widget = param.get_input(self._handle_changed, self._activate_apply)
                    input_widget.show_all()
                    vbox.pack_start(input_widget, input_widget.expand, True, 1)

                label.set_markup('<span foreground="{color}">{name}</span>'.format(
                    color='black' if box_all_valid else 'red', name=Utils.encode(tab)
                ))
                vbox.show()  # show params box with new params

        if self._block.is_valid():
            self._error_box.hide()
        else:
            self._error_box.show()
        messages = '\n\n'.join(self._block.get_error_messages())
        self._error_messages_text_display.set_text(messages)

        self._update_docs_page()
        self._update_generated_code_page()

    def _update_docs_page(self):
        """Show documentation from XML and try to display best matching docstring"""
        buf = self._docs_text_display.get_buffer()
        buf.delete(buf.get_start_iter(), buf.get_end_iter())
        pos = buf.get_end_iter()

        docstrings = self._block.get_doc()
        if not docstrings:
            return

        # show documentation string from block xml
        from_xml = docstrings.pop('', '')
        for line in from_xml.splitlines():
            if line.lstrip() == line and line.endswith(':'):
                buf.insert_with_tags_by_name(pos, line + '\n', 'b')
            else:
                buf.insert(pos, line + '\n')
        if from_xml:
            buf.insert(pos, '\n')

        # if given the current parameters an exact match can be made
        block_constructor = self._block.get_make().rsplit('.', 2)[-1]
        block_class = block_constructor.partition('(')[0].strip()
        if block_class in docstrings:
            docstrings = {block_class: docstrings[block_class]}

        # show docstring(s) extracted from python sources
        for cls_name, docstring in six.iteritems(docstrings):
            buf.insert_with_tags_by_name(pos, cls_name + '\n', 'b')
            buf.insert(pos, docstring + '\n\n')
        pos.backward_chars(2)
        buf.delete(pos, buf.get_end_iter())

    def _update_generated_code_page(self):
        if not self._code_text_display:
            return  # user disabled code preview

        buf = self._code_text_display.get_buffer()
        block = self._block
        key = block.get_key()

        if key == 'epy_block':
            src = block.get_param('_source_code').get_value()
        elif key == 'epy_module':
            src = block.get_param('source_code').get_value()
        else:
            src = ''

        def insert(header, text):
            if not text:
                return
            buf.insert_with_tags_by_name(buf.get_end_iter(), header, 'b')
            buf.insert(buf.get_end_iter(), text)

        buf.delete(buf.get_start_iter(), buf.get_end_iter())
        insert('# Imports\n', '\n'.join(block.get_imports()))
        if block.is_variable:
            insert('\n\n# Variables\n', block.get_var_make())
        insert('\n\n# Blocks\n', block.get_make())
        if src:
            insert('\n\n# External Code ({}.py)\n'.format(block.get_id()), src)

    def _handle_key_press(self, widget, event):
        close_dialog = (
            event.keyval == Gdk.KEY_Return and
            event.get_state() & Gdk.ModifierType.CONTROL_MASK == 0 and
            not isinstance(widget.get_focus(), Gtk.TextView)
        )
        if close_dialog:
            self.response(Gtk.ResponseType.ACCEPT)
            return True  # handled here

        return False  # forward the keypress

    def _handle_response(self, widget, response):
        if response in (Gtk.ResponseType.APPLY, Gtk.ResponseType.ACCEPT):
            for tab, label, vbox in self._params_boxes:
                for child in vbox.get_children():
                    child.apply_pending_changes()
            self.set_response_sensitive(Gtk.ResponseType.APPLY, False)
            return True
        return False
