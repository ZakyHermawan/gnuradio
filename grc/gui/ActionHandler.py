"""
Copyright 2007-2011 Free Software Foundation, Inc.
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


from __future__ import absolute_import, print_function

import os
import subprocess

from gi.repository import Gtk
from gi.repository import GObject

from . import Dialogs, Preferences, Actions, Executor, Constants
from .FileDialogs import (OpenFlowGraphFileDialog, SaveFlowGraphFileDialog,
                          SaveConsoleFileDialog, SaveScreenShotDialog,
                          OpenQSSFileDialog)
from .MainWindow import MainWindow
from .ParserErrorsDialog import ParserErrorsDialog
from .PropsDialog import PropsDialog

from ..core import ParseXML, Messages


class ActionHandler:
    """
    The action handler will setup all the major window components,
    and handle button presses and flow graph operations from the GUI.
    """

    def __init__(self, file_paths, platform):
        """
        ActionHandler constructor.
        Create the main window, setup the message handler, import the preferences,
        and connect all of the action handlers. Finally, enter the gtk main loop and block.

        Args:
            file_paths: a list of flow graph file passed from command line
            platform: platform module
        """
        self.clipboard = None
        self.dialog = None
        for action in Actions.get_all_actions(): action.connect('activate', self._handle_action)
        #setup the main window
        self.platform = platform
        self.main_window = MainWindow(platform, self._handle_action)
        self.main_window.connect('delete-event', self._quit)
        self.main_window.connect('key-press-event', self._handle_key_press)
        self.get_focus_flag = self.main_window.get_focus_flag
        #setup the messages
        Messages.register_messenger(self.main_window.add_console_line)
        Messages.send_init(platform)
        #initialize
        self.init_file_paths = file_paths
        self.init = False
        Actions.APPLICATION_INITIALIZE()

    def _handle_key_press(self, widget, event):
        """
        Handle key presses from the keyboard and translate key combinations into actions.
        This key press handler is called prior to the gtk key press handler.
        This handler bypasses built in accelerator key handling when in focus because
        * some keys are ignored by the accelerators like the direction keys,
        * some keys are not registered to any accelerators but are still used.
        When not in focus, gtk and the accelerators handle the the key press.

        Returns:
            false to let gtk handle the key action
        """
        # prevent key event stealing while the search box is active
        # .has_focus() only in newer versions 2.17+?
        # .is_focus() seems to work, but exactly the same
        if self.main_window.btwin.search_entry.has_focus():
            return False
        return Actions.handle_key_press(event)

    def _quit(self, window, event):
        """
        Handle the delete event from the main window.
        Generated by pressing X to close, alt+f4, or right click+close.
        This method in turns calls the state handler to quit.

        Returns:
            true
        """
        Actions.APPLICATION_QUIT()
        return True

    def _handle_action(self, action, *args):
        #print action
        main = self.main_window
        page = main.current_page
        flow_graph = page.flow_graph if page else None

        def flow_graph_update(fg=flow_graph):
            main.vars.update_gui(fg.blocks)
            fg.update()

        ##################################################
        # Initialize/Quit
        ##################################################
        if action == Actions.APPLICATION_INITIALIZE:
            if not self.init_file_paths:
                self.init_file_paths = list(filter(os.path.exists, Preferences.get_open_files()))
            if not self.init_file_paths: self.init_file_paths = ['']
            for file_path in self.init_file_paths:
                if file_path: main.new_page(file_path) #load pages from file paths
            if Preferences.file_open() in self.init_file_paths:
                main.new_page(Preferences.file_open(), show=True)
            if not self.main_window.current_page:
                main.new_page()  # ensure that at least a blank page exists

            main.btwin.search_entry.hide()

            # Disable all actions, then re-enable a few
            for action in Actions.get_all_actions():
                action.set_sensitive(False)  # set all actions disabled
            for action in (
                Actions.APPLICATION_QUIT, Actions.FLOW_GRAPH_NEW,
                Actions.FLOW_GRAPH_OPEN, Actions.FLOW_GRAPH_SAVE_AS,
                Actions.FLOW_GRAPH_CLOSE, Actions.ABOUT_WINDOW_DISPLAY,
                Actions.FLOW_GRAPH_SCREEN_CAPTURE, Actions.HELP_WINDOW_DISPLAY,
                Actions.TYPES_WINDOW_DISPLAY, Actions.TOGGLE_BLOCKS_WINDOW,
                Actions.TOGGLE_CONSOLE_WINDOW, Actions.TOGGLE_HIDE_DISABLED_BLOCKS,
                Actions.TOOLS_RUN_FDESIGN, Actions.TOGGLE_SCROLL_LOCK,
                Actions.CLEAR_CONSOLE, Actions.SAVE_CONSOLE,
                Actions.TOGGLE_AUTO_HIDE_PORT_LABELS, Actions.TOGGLE_SNAP_TO_GRID,
                Actions.TOGGLE_SHOW_BLOCK_COMMENTS,
                Actions.TOGGLE_SHOW_CODE_PREVIEW_TAB,
                Actions.TOGGLE_SHOW_FLOWGRAPH_COMPLEXITY,
                Actions.FLOW_GRAPH_OPEN_QSS_THEME,
                Actions.TOGGLE_FLOW_GRAPH_VAR_EDITOR,
                Actions.TOGGLE_FLOW_GRAPH_VAR_EDITOR_SIDEBAR,
                Actions.TOGGLE_HIDE_VARIABLES,
                Actions.SELECT_ALL,
            ):
                action.set_sensitive(True)
                if hasattr(action, 'load_from_preferences'):
                    action.load_from_preferences()
            if ParseXML.xml_failures:
                Messages.send_xml_errors_if_any(ParseXML.xml_failures)
                Actions.XML_PARSER_ERRORS_DISPLAY.set_sensitive(True)
            self.init = True
        elif action == Actions.APPLICATION_QUIT:
            if main.close_pages():
                Gtk.main_quit()
                exit(0)
        ##################################################
        # Selections
        ##################################################
        elif action == Actions.ELEMENT_SELECT:
            pass #do nothing, update routines below
        elif action == Actions.NOTHING_SELECT:
            flow_graph.unselect()
        elif action == Actions.SELECT_ALL:
            flow_graph.select_all()
        ##################################################
        # Enable/Disable
        ##################################################
        elif action == Actions.BLOCK_ENABLE:
            if flow_graph.enable_selected(True):
                flow_graph_update()
                page.state_cache.save_new_state(flow_graph.export_data())
                page.saved = False
        elif action == Actions.BLOCK_DISABLE:
            if flow_graph.enable_selected(False):
                flow_graph_update()
                page.state_cache.save_new_state(flow_graph.export_data())
                page.saved = False
        elif action == Actions.BLOCK_BYPASS:
            if flow_graph.bypass_selected():
                flow_graph_update()
                page.state_cache.save_new_state(flow_graph.export_data())
                page.saved = False
        ##################################################
        # Cut/Copy/Paste
        ##################################################
        elif action == Actions.BLOCK_CUT:
            Actions.BLOCK_COPY()
            Actions.ELEMENT_DELETE()
        elif action == Actions.BLOCK_COPY:
            self.clipboard = flow_graph.copy_to_clipboard()
        elif action == Actions.BLOCK_PASTE:
            if self.clipboard:
                flow_graph.paste_from_clipboard(self.clipboard)
                flow_graph_update()
                page.state_cache.save_new_state(flow_graph.export_data())
                page.saved = False
                ##################################################
                # Create heir block
                ##################################################
        elif action == Actions.BLOCK_CREATE_HIER:

                        # keeping track of coordinates for pasting later
                        coords = flow_graph.get_selected_blocks()[0].get_coordinate()
                        x,y = coords
                        x_min = x
                        y_min = y

                        pads = [];
                        params = [];

                        # Save the state of the leaf blocks
                        for block in flow_graph.get_selected_blocks():

                            # Check for string variables within the blocks
                            for param in block.get_params():
                                for variable in flow_graph.get_variables():
                                    # If a block parameter exists that is a variable, create a parameter for it
                                    if param.get_value() == variable.get_id():
                                        params.append(param.get_value())
                                for flow_param in flow_graph.get_parameters():
                                    # If a block parameter exists that is a parameter, create a parameter for it
                                    if param.get_value() == flow_param.get_id():
                                        params.append(param.get_value())


                            # keep track of x,y mins for pasting later
                            (x,y) = block.get_coordinate()
                            if x < x_min:
                                x_min = x
                            if y < y_min:
                                y_min = y

                            for connection in block.connections:

                                # Get id of connected blocks
                                source_id = connection.source_block.get_id()
                                sink_id = connection.sink_block.get_id()

                                # If connected block is not in the list of selected blocks create a pad for it
                                if flow_graph.get_block(source_id) not in flow_graph.get_selected_blocks():
                                    pads.append({'key': connection.sink_port.key, 'coord': connection.source_port.get_coordinate(), 'block_id' : block.get_id(), 'direction': 'source'})

                                if flow_graph.get_block(sink_id) not in flow_graph.get_selected_blocks():
                                    pads.append({'key': connection.source_port.key, 'coord': connection.sink_port.get_coordinate(), 'block_id' : block.get_id(), 'direction': 'sink'})


                        # Copy the selected blocks and paste them into a new page
                        #   then move the flowgraph to a reasonable position
                        Actions.BLOCK_COPY()
                        main.new_page()
                        Actions.BLOCK_PASTE()
                        coords = (x_min,y_min)
                        flow_graph.move_selected(coords)


                        # Set flow graph to heir block type
                        top_block  = flow_graph.get_block("top_block")
                        top_block.get_param('generate_options').set_value('hb')

                        # this needs to be a unique name
                        top_block.get_param('id').set_value('new_heir')

                        # Remove the default samp_rate variable block that is created
                        remove_me  = flow_graph.get_block("samp_rate")
                        flow_graph.remove_element(remove_me)


                        # Add the param blocks along the top of the window
                        x_pos = 150
                        for param in params:
                            param_id = flow_graph.add_new_block('parameter',(x_pos,10))
                            param_block = flow_graph.get_block(param_id)
                            param_block.get_param('id').set_value(param)
                            x_pos = x_pos + 100

                        for pad in pads:
                            # Add the pad sources and sinks within the new heir block
                            if pad['direction'] == 'sink':

                                # Add new PAD_SINK block to the canvas
                                pad_id = flow_graph.add_new_block('pad_sink', pad['coord'])

                                # setup the references to the sink and source
                                pad_block = flow_graph.get_block(pad_id)
                                pad_sink = pad_block.get_sinks()[0]

                                source_block = flow_graph.get_block(pad['block_id'])
                                source = source_block.get_source(pad['key'])

                                # Ensure the port types match
                                while pad_sink.get_type() != source.get_type():

                                    # Special case for some blocks that have non-standard type names, e.g. uhd
                                    if pad_sink.get_type() == 'complex' and source.get_type() == 'fc32':
                                        break;
                                    pad_block.type_controller_modify(1)

                                # Connect the pad to the proper sinks
                                new_connection = flow_graph.connect(source,pad_sink)

                            elif pad['direction'] == 'source':
                                pad_id = flow_graph.add_new_block('pad_source', pad['coord'])

                                # setup the references to the sink and source
                                pad_block = flow_graph.get_block(pad_id)
                                pad_source = pad_block.get_sources()[0]

                                sink_block = flow_graph.get_block(pad['block_id'])
                                sink = sink_block.get_sink(pad['key'])

                                # Ensure the port types match
                                while sink.get_type() != pad_source.get_type():
                                    # Special case for some blocks that have non-standard type names, e.g. uhd
                                    if pad_source.get_type() == 'complex' and sink.get_type() == 'fc32':
                                        break;
                                    pad_block.type_controller_modify(1)

                                # Connect the pad to the proper sinks
                                new_connection = flow_graph.connect(pad_source,sink)

                        # update the new heir block flow graph
                        flow_graph_update()


        ##################################################
        # Move/Rotate/Delete/Create
        ##################################################
        elif action == Actions.BLOCK_MOVE:
            page.state_cache.save_new_state(flow_graph.export_data())
            page.saved = False
        elif action in Actions.BLOCK_ALIGNMENTS:
            if flow_graph.align_selected(action):
                page.state_cache.save_new_state(flow_graph.export_data())
                page.saved = False
        elif action == Actions.BLOCK_ROTATE_CCW:
            if flow_graph.rotate_selected(90):
                flow_graph_update()
                page.state_cache.save_new_state(flow_graph.export_data())
                page.saved = False
        elif action == Actions.BLOCK_ROTATE_CW:
            if flow_graph.rotate_selected(-90):
                flow_graph_update()
                page.state_cache.save_new_state(flow_graph.export_data())
                page.saved = False
        elif action == Actions.ELEMENT_DELETE:
            if flow_graph.remove_selected():
                flow_graph_update()
                page.state_cache.save_new_state(flow_graph.export_data())
                Actions.NOTHING_SELECT()
                page.saved = False
        elif action == Actions.ELEMENT_CREATE:
            flow_graph_update()
            page.state_cache.save_new_state(flow_graph.export_data())
            Actions.NOTHING_SELECT()
            page.saved = False
        elif action == Actions.BLOCK_INC_TYPE:
            if flow_graph.type_controller_modify_selected(1):
                flow_graph_update()
                page.state_cache.save_new_state(flow_graph.export_data())
                page.saved = False
        elif action == Actions.BLOCK_DEC_TYPE:
            if flow_graph.type_controller_modify_selected(-1):
                flow_graph_update()
                page.state_cache.save_new_state(flow_graph.export_data())
                page.saved = False
        elif action == Actions.PORT_CONTROLLER_INC:
            if flow_graph.port_controller_modify_selected(1):
                flow_graph_update()
                page.state_cache.save_new_state(flow_graph.export_data())
                page.saved = False
        elif action == Actions.PORT_CONTROLLER_DEC:
            if flow_graph.port_controller_modify_selected(-1):
                flow_graph_update()
                page.state_cache.save_new_state(flow_graph.export_data())
                page.saved = False
        ##################################################
        # Window stuff
        ##################################################
        elif action == Actions.ABOUT_WINDOW_DISPLAY:
            Dialogs.AboutDialog(self.platform.config)
        elif action == Actions.HELP_WINDOW_DISPLAY:
            Dialogs.HelpDialog()
        elif action == Actions.TYPES_WINDOW_DISPLAY:
            Dialogs.TypesDialog(self.platform)
        elif action == Actions.ERRORS_WINDOW_DISPLAY:
            Dialogs.ErrorsDialog(flow_graph)
        elif action == Actions.TOGGLE_CONSOLE_WINDOW:
            main.update_panel_visibility(main.CONSOLE, action.get_active())
            action.save_to_preferences()
        elif action == Actions.TOGGLE_BLOCKS_WINDOW:
            main.update_panel_visibility(main.BLOCKS, action.get_active())
            action.save_to_preferences()
        elif action == Actions.TOGGLE_SCROLL_LOCK:
            active = action.get_active()
            main.text_display.scroll_lock = active
            if active:
                main.text_display.scroll_to_end()
            action.save_to_preferences()
        elif action == Actions.CLEAR_CONSOLE:
            main.text_display.clear()
        elif action == Actions.SAVE_CONSOLE:
            file_path = SaveConsoleFileDialog(page.file_path).run()
            if file_path is not None:
                main.text_display.save(file_path)
        elif action == Actions.TOGGLE_HIDE_DISABLED_BLOCKS:
            Actions.NOTHING_SELECT()
        elif action == Actions.TOGGLE_AUTO_HIDE_PORT_LABELS:
            action.save_to_preferences()
            for page in main.get_pages():
                page.flow_graph.create_shapes()
        elif action in (Actions.TOGGLE_SNAP_TO_GRID,
                        Actions.TOGGLE_SHOW_BLOCK_COMMENTS,
                        Actions.TOGGLE_SHOW_CODE_PREVIEW_TAB):
            action.save_to_preferences()
        elif action == Actions.TOGGLE_SHOW_FLOWGRAPH_COMPLEXITY:
            action.save_to_preferences()
            for page in main.get_pages():
                flow_graph_update(page.flow_graph)
        elif action == Actions.TOGGLE_HIDE_VARIABLES:
            # Call the variable editor TOGGLE in case it needs to be showing
            Actions.TOGGLE_FLOW_GRAPH_VAR_EDITOR()
            Actions.NOTHING_SELECT()
            action.save_to_preferences()
        elif action == Actions.TOGGLE_FLOW_GRAPH_VAR_EDITOR:
            # See if the variables are hidden
            if Actions.TOGGLE_HIDE_VARIABLES.get_active():
                # Force this to be shown
                main.update_panel_visibility(main.VARIABLES, True)
                action.set_active(True)
                action.set_sensitive(False)
            else:
                if action.get_sensitive():
                    main.update_panel_visibility(main.VARIABLES, action.get_active())
                else:  # This is occurring after variables are un-hidden
                    # Leave it enabled
                    action.set_sensitive(True)
                    action.set_active(True)
            #Actions.TOGGLE_FLOW_GRAPH_VAR_EDITOR_SIDEBAR.set_sensitive(action.get_active())
            action.save_to_preferences()
        elif action == Actions.TOGGLE_FLOW_GRAPH_VAR_EDITOR_SIDEBAR:
            if self.init:
                md = Gtk.MessageDialog(main,
                    Gtk.DIALOG_DESTROY_WITH_PARENT, Gtk.MESSAGE_INFO,
                    Gtk.BUTTONS_CLOSE, "Moving the variable editor requires a restart of GRC.")
                md.run()
                md.destroy()
                action.save_to_preferences()
        ##################################################
        # Param Modifications
        ##################################################
        elif action == Actions.BLOCK_PARAM_MODIFY:
            if action.args:
                selected_block = action.args[0]
            else:
                selected_block = flow_graph.get_selected_block()
            if selected_block:
                self.dialog = PropsDialog(self.main_window, selected_block)
                response = Gtk.ResponseType.APPLY
                while response == Gtk.ResponseType.APPLY:  # rerun the dialog if Apply was hit
                    response = self.dialog.run()
                    if response in (Gtk.ResponseType.APPLY, Gtk.ResponseType.ACCEPT):
                        flow_graph_update()
                        page.state_cache.save_new_state(flow_graph.export_data())
                        page.saved = False
                    else:  # restore the current state
                        n = page.state_cache.get_current_state()
                        flow_graph.import_data(n)
                        flow_graph_update()
                    if response == Gtk.ResponseType.APPLY:
                        # null action, that updates the main window
                        Actions.ELEMENT_SELECT()
                self.dialog.destroy()
                self.dialog = None
        elif action == Actions.EXTERNAL_UPDATE:
            page.state_cache.save_new_state(flow_graph.export_data())
            flow_graph_update()
            if self.dialog is not None:
                self.dialog.update_gui(force=True)
            page.saved = False
        elif action == Actions.VARIABLE_EDITOR_UPDATE:
            page.state_cache.save_new_state(flow_graph.export_data())
            flow_graph_update()
            page.saved = False
        ##################################################
        # View Parser Errors
        ##################################################
        elif action == Actions.XML_PARSER_ERRORS_DISPLAY:
            ParserErrorsDialog(ParseXML.xml_failures).run()
        ##################################################
        # Undo/Redo
        ##################################################
        elif action == Actions.FLOW_GRAPH_UNDO:
            n = page.state_cache.get_prev_state()
            if n:
                flow_graph.unselect()
                flow_graph.import_data(n)
                flow_graph_update()
                page.saved = False
        elif action == Actions.FLOW_GRAPH_REDO:
            n = page.state_cache.get_next_state()
            if n:
                flow_graph.unselect()
                flow_graph.import_data(n)
                flow_graph_update()
                page.saved = False
        ##################################################
        # New/Open/Save/Close
        ##################################################
        elif action == Actions.FLOW_GRAPH_NEW:
            main.new_page()
            if args:
                flow_graph._options_block.get_param('generate_options').set_value(args[0])
                flow_graph_update()
        elif action == Actions.FLOW_GRAPH_OPEN:
            # TODO: Disable opening the flowgraph
            pass
            '''
            file_paths = args if args else OpenFlowGraphFileDialog(page.file_path).run()
            if file_paths: # Open a new page for each file, show only the first
                for i,file_path in enumerate(file_paths):
                    main.new_page(file_path, show=(i==0))
                    Preferences.add_recent_file(file_path)
                    main.tool_bar.refresh_submenus()
                    main.menu_bar.refresh_submenus()
                    main.vars.update_gui()
            '''
        elif action == Actions.FLOW_GRAPH_OPEN_QSS_THEME:
            file_paths = OpenQSSFileDialog(self.platform.config.install_prefix +
                                           '/share/gnuradio/themes/').run()
            if file_paths:
                try:
                    prefs = self.platform.config.prefs
                    prefs.set_string("qtgui", "qss", file_paths[0])
                    prefs.save()
                except Exception as e:
                    Messages.send("Failed to save QSS preference: " + str(e))
        elif action == Actions.FLOW_GRAPH_CLOSE:
            main.close_page()
        elif action == Actions.FLOW_GRAPH_SAVE:
            #read-only or undefined file path, do save-as
            if page.get_read_only() or not page.file_path:
                Actions.FLOW_GRAPH_SAVE_AS()
            #otherwise try to save
            else:
                try:
                    ParseXML.to_file(flow_graph.export_data(), page.file_path)
                    flow_graph.grc_file_path = page.file_path
                    page.saved = True
                except IOError:
                    Messages.send_fail_save(page.file_path)
                    page.saved = False
        elif action == Actions.FLOW_GRAPH_SAVE_AS:
            file_path = SaveFlowGraphFileDialog(page.file_path).run()
            if file_path is not None:
                page.file_path = os.path.abspath(file_path)
                Actions.FLOW_GRAPH_SAVE()
                Preferences.add_recent_file(file_path)
                main.tool_bar.refresh_submenus()
                main.menu_bar.refresh_submenus()
        elif action == Actions.FLOW_GRAPH_SCREEN_CAPTURE:
            file_path, background_transparent = SaveScreenShotDialog(page.file_path).run()
            if file_path is not None:
                pixbuf = flow_graph.get_drawing_area().get_screenshot(background_transparent)
                pixbuf.save(file_path, Constants.IMAGE_FILE_EXTENSION[1:])
        ##################################################
        # Gen/Exec/Stop
        ##################################################
        elif action == Actions.FLOW_GRAPH_GEN:
            if not page.process:
                if not page.saved or not page.file_path:
                    Actions.FLOW_GRAPH_SAVE()  # only save if file path missing or not saved
                if page.saved and page.file_path:
                    generator = page.get_generator()
                    try:
                        Messages.send_start_gen(generator.file_path)
                        generator.write()
                    except Exception as e:
                        Messages.send_fail_gen(e)
                else:
                    self.generator = None
        elif action == Actions.FLOW_GRAPH_EXEC:
            if not page.process:
                Actions.FLOW_GRAPH_GEN()
                xterm = self.platform.config.xterm_executable
                if Preferences.xterm_missing() != xterm:
                    if not os.path.exists(xterm):
                        Dialogs.MissingXTermDialog(xterm)
                    Preferences.xterm_missing(xterm)
                if page.saved and page.file_path:
                    Executor.ExecFlowGraphThread(
                        flow_graph_page=page,
                        xterm_executable=xterm,
                        callback=self.update_exec_stop
                    )
        elif action == Actions.FLOW_GRAPH_KILL:
            if page.process:
                try:
                    page.process.kill()
                except:
                    print("could not kill process: %d" % page.process.pid)
        elif action == Actions.PAGE_CHANGE:  # pass and run the global actions
            pass
        elif action == Actions.RELOAD_BLOCKS:
            self.platform.build_block_library()
            main.btwin.repopulate()
            Actions.XML_PARSER_ERRORS_DISPLAY.set_sensitive(bool(
                ParseXML.xml_failures))
            Messages.send_xml_errors_if_any(ParseXML.xml_failures)
            # Force a redraw of the graph, by getting the current state and re-importing it
            main.update_pages()

        elif action == Actions.FIND_BLOCKS:
            main.update_panel_visibility(main.BLOCKS, True)
            main.btwin.search_entry.show()
            main.btwin.search_entry.grab_focus()
        elif action == Actions.OPEN_HIER:
            for b in flow_graph.get_selected_blocks():
                if b._grc_source:
                    main.new_page(b._grc_source, show=True)
        elif action == Actions.BUSSIFY_SOURCES:
            n = {'name':'bus', 'type':'bus'}
            for b in flow_graph.get_selected_blocks():
                b.bussify(n, 'source')
            flow_graph._old_selected_port = None
            flow_graph._new_selected_port = None
            Actions.ELEMENT_CREATE()

        elif action == Actions.BUSSIFY_SINKS:
            n = {'name':'bus', 'type':'bus'}
            for b in flow_graph.get_selected_blocks():
                b.bussify(n, 'sink')
            flow_graph._old_selected_port = None
            flow_graph._new_selected_port = None
            Actions.ELEMENT_CREATE()

        elif action == Actions.TOOLS_RUN_FDESIGN:
            subprocess.Popen('gr_filter_design',
                             shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        else:
            print('!!! Action "%s" not handled !!!' % action)
        ##################################################
        # Global Actions for all States
        ##################################################
        page = main.current_page  # page and flow graph might have changed
        flow_graph = page.flow_graph if page else None

        selected_blocks = flow_graph.get_selected_blocks()
        selected_block = selected_blocks[0] if selected_blocks else None

        #update general buttons
        Actions.ERRORS_WINDOW_DISPLAY.set_sensitive(not flow_graph.is_valid())
        Actions.ELEMENT_DELETE.set_sensitive(bool(flow_graph.get_selected_elements()))
        Actions.BLOCK_PARAM_MODIFY.set_sensitive(bool(selected_block))
        Actions.BLOCK_ROTATE_CCW.set_sensitive(bool(selected_blocks))
        Actions.BLOCK_ROTATE_CW.set_sensitive(bool(selected_blocks))
        #update alignment options
        for act in Actions.BLOCK_ALIGNMENTS:
            if act:
                act.set_sensitive(len(selected_blocks) > 1)
        #update cut/copy/paste
        Actions.BLOCK_CUT.set_sensitive(bool(selected_blocks))
        Actions.BLOCK_COPY.set_sensitive(bool(selected_blocks))
        Actions.BLOCK_PASTE.set_sensitive(bool(self.clipboard))
        #update enable/disable/bypass
        can_enable = any(block.state != block.ENABLED
                         for block in selected_blocks)
        can_disable = any(block.state != block.DISABLED
                          for block in selected_blocks)
        can_bypass_all = (
            all(block.can_bypass() for block in selected_blocks) and
            any(not block.get_bypassed() for block in selected_blocks)
        )
        Actions.BLOCK_ENABLE.set_sensitive(can_enable)
        Actions.BLOCK_DISABLE.set_sensitive(can_disable)
        Actions.BLOCK_BYPASS.set_sensitive(can_bypass_all)

        Actions.BLOCK_CREATE_HIER.set_sensitive(bool(selected_blocks))
        Actions.OPEN_HIER.set_sensitive(bool(selected_blocks))
        Actions.BUSSIFY_SOURCES.set_sensitive(bool(selected_blocks))
        Actions.BUSSIFY_SINKS.set_sensitive(bool(selected_blocks))
        Actions.RELOAD_BLOCKS.set_sensitive(True)
        Actions.FIND_BLOCKS.set_sensitive(True)

        self.update_exec_stop()

        Actions.FLOW_GRAPH_SAVE.set_sensitive(not page.saved)
        main.update()

        flow_graph.update_selected()
        flow_graph.queue_draw()

        return True  # action was handled

    def update_exec_stop(self):
        """
        Update the exec and stop buttons.
        Lock and unlock the mutex for race conditions with exec flow graph threads.
        """
        page = self.main_window.current_page
        sensitive = page.flow_graph.is_valid() and not page.process
        Actions.FLOW_GRAPH_GEN.set_sensitive(sensitive)
        Actions.FLOW_GRAPH_EXEC.set_sensitive(sensitive)
        Actions.FLOW_GRAPH_KILL.set_sensitive(page.process is not None)
