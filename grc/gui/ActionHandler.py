"""
Copyright 2007, 2008, 2009, 2011 Free Software Foundation, Inc.
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

import os
import signal 
from Constants import IMAGE_FILE_EXTENSION
import Actions
import pygtk
pygtk.require('2.0')
import gtk
import gobject
import Preferences
from threading import Thread
import Messages
from .. base import ParseXML
from MainWindow import MainWindow
from PropsDialog import PropsDialog
import Dialogs
from FileDialogs import OpenFlowGraphFileDialog, SaveFlowGraphFileDialog, SaveImageFileDialog

gobject.threads_init()

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
		@param file_paths a list of flow graph file passed from command line
		@param platform platform module
		"""
		self.clipboard = None
		for action in Actions.get_all_actions(): action.connect('activate', self._handle_action)
		#setup the main window
		self.main_window = MainWindow(platform)
		self.main_window.connect('delete-event', self._quit)
		self.main_window.connect('key-press-event', self._handle_key_press)
		self.get_page = self.main_window.get_page
		self.get_flow_graph = self.main_window.get_flow_graph
		self.get_focus_flag = self.main_window.get_focus_flag
		#setup the messages
		Messages.register_messenger(self.main_window.add_report_line)
		Messages.send_init(platform)
		#initialize
		self.init_file_paths = file_paths
		Actions.APPLICATION_INITIALIZE()
		#enter the mainloop
		gtk.main()

	def _handle_key_press(self, widget, event):
		"""
		Handle key presses from the keyboard and translate key combinations into actions.
		This key press handler is called prior to the gtk key press handler.
		This handler bypasses built in accelerator key handling when in focus because
		* some keys are ignored by the accelerators like the direction keys,
		* some keys are not registered to any accelerators but are still used.
		When not in focus, gtk and the accelerators handle the the key press.
		@return false to let gtk handle the key action
		"""
		try: assert self.get_focus_flag()
		except AssertionError: return False
		return Actions.handle_key_press(event)

	def _quit(self, window, event):
		"""
		Handle the delete event from the main window.
		Generated by pressing X to close, alt+f4, or right click+close.
		This method in turns calls the state handler to quit.
		@return true
		"""
		Actions.APPLICATION_QUIT()
		return True

	def _handle_action(self, action):
		#print action
		##################################################
		# Initalize/Quit
		##################################################
		if action == Actions.APPLICATION_INITIALIZE:
			for action in Actions.get_all_actions(): action.set_sensitive(False) #set all actions disabled
			#enable a select few actions
			for action in (
				Actions.APPLICATION_QUIT, Actions.FLOW_GRAPH_NEW,
				Actions.FLOW_GRAPH_OPEN, Actions.FLOW_GRAPH_SAVE_AS,
				Actions.FLOW_GRAPH_CLOSE, Actions.ABOUT_WINDOW_DISPLAY,
				Actions.FLOW_GRAPH_SCREEN_CAPTURE, Actions.HELP_WINDOW_DISPLAY,
				Actions.TYPES_WINDOW_DISPLAY,
			): action.set_sensitive(True)
			if not self.init_file_paths:
				self.init_file_paths = Preferences.files_open()
			if not self.init_file_paths: self.init_file_paths = ['']
			for file_path in self.init_file_paths:
				if file_path: self.main_window.new_page(file_path) #load pages from file paths
			if Preferences.file_open() in self.init_file_paths:
				self.main_window.new_page(Preferences.file_open(), show=True)
			if not self.get_page():	self.main_window.new_page() #ensure that at least a blank page exists
		elif action == Actions.APPLICATION_QUIT:
			if self.main_window.close_pages():
				gtk.main_quit()
				exit(0)
		##################################################
		# Selections
		##################################################
		elif action == Actions.ELEMENT_SELECT:
			pass #do nothing, update routines below
		elif action == Actions.NOTHING_SELECT:
			self.get_flow_graph().unselect()
		##################################################
		# Enable/Disable
		##################################################
		elif action == Actions.BLOCK_ENABLE:
			if self.get_flow_graph().enable_selected(True):
				self.get_flow_graph().update()
				self.get_page().get_state_cache().save_new_state(self.get_flow_graph().export_data())
				self.get_page().set_saved(False)
		elif action == Actions.BLOCK_DISABLE:
			if self.get_flow_graph().enable_selected(False):
				self.get_flow_graph().update()
				self.get_page().get_state_cache().save_new_state(self.get_flow_graph().export_data())
				self.get_page().set_saved(False)
		##################################################
		# Cut/Copy/Paste
		##################################################
		elif action == Actions.BLOCK_CUT:
			Actions.BLOCK_COPY()
			Actions.ELEMENT_DELETE()
		elif action == Actions.BLOCK_COPY:
			self.clipboard = self.get_flow_graph().copy_to_clipboard()
		elif action == Actions.BLOCK_PASTE:
			if self.clipboard:
				self.get_flow_graph().paste_from_clipboard(self.clipboard)
				self.get_flow_graph().update()
				self.get_page().get_state_cache().save_new_state(self.get_flow_graph().export_data())
				self.get_page().set_saved(False)
		##################################################
		# Move/Rotate/Delete/Create
		##################################################
		elif action == Actions.BLOCK_MOVE:
			self.get_page().get_state_cache().save_new_state(self.get_flow_graph().export_data())
			self.get_page().set_saved(False)
		elif action == Actions.BLOCK_ROTATE_CCW:
			if self.get_flow_graph().rotate_selected(90):
				self.get_flow_graph().update()
				self.get_page().get_state_cache().save_new_state(self.get_flow_graph().export_data())
				self.get_page().set_saved(False)
		elif action == Actions.BLOCK_ROTATE_CW:
			if self.get_flow_graph().rotate_selected(-90):
				self.get_flow_graph().update()
				self.get_page().get_state_cache().save_new_state(self.get_flow_graph().export_data())
				self.get_page().set_saved(False)
		elif action == Actions.ELEMENT_DELETE:
			if self.get_flow_graph().remove_selected():
				self.get_flow_graph().update()
				self.get_page().get_state_cache().save_new_state(self.get_flow_graph().export_data())
				Actions.NOTHING_SELECT()
				self.get_page().set_saved(False)
		elif action == Actions.ELEMENT_CREATE:
			self.get_flow_graph().update()
			self.get_page().get_state_cache().save_new_state(self.get_flow_graph().export_data())
			Actions.NOTHING_SELECT()
			self.get_page().set_saved(False)
		elif action == Actions.BLOCK_INC_TYPE:
			if self.get_flow_graph().type_controller_modify_selected(1):
				self.get_flow_graph().update()
				self.get_page().get_state_cache().save_new_state(self.get_flow_graph().export_data())
				self.get_page().set_saved(False)
		elif action == Actions.BLOCK_DEC_TYPE:
			if self.get_flow_graph().type_controller_modify_selected(-1):
				self.get_flow_graph().update()
				self.get_page().get_state_cache().save_new_state(self.get_flow_graph().export_data())
				self.get_page().set_saved(False)
		elif action == Actions.PORT_CONTROLLER_INC:
			if self.get_flow_graph().port_controller_modify_selected(1):
				self.get_flow_graph().update()
				self.get_page().get_state_cache().save_new_state(self.get_flow_graph().export_data())
				self.get_page().set_saved(False)
		elif action == Actions.PORT_CONTROLLER_DEC:
			if self.get_flow_graph().port_controller_modify_selected(-1):
				self.get_flow_graph().update()
				self.get_page().get_state_cache().save_new_state(self.get_flow_graph().export_data())
				self.get_page().set_saved(False)
		##################################################
		# Window stuff
		##################################################
		elif action == Actions.ABOUT_WINDOW_DISPLAY:
			Dialogs.AboutDialog(self.get_flow_graph().get_parent())
		elif action == Actions.HELP_WINDOW_DISPLAY:
			Dialogs.HelpDialog()
		elif action == Actions.TYPES_WINDOW_DISPLAY:
			Dialogs.TypesDialog(self.get_flow_graph().get_parent())
		elif action == Actions.ERRORS_WINDOW_DISPLAY:
			Dialogs.ErrorsDialog(self.get_flow_graph())
		##################################################
		# Param Modifications
		##################################################
		elif action == Actions.BLOCK_PARAM_MODIFY:
			selected_block = self.get_flow_graph().get_selected_block()
			if selected_block:
				if PropsDialog(selected_block).run():
					#save the new state
					self.get_flow_graph().update()
					self.get_page().get_state_cache().save_new_state(self.get_flow_graph().export_data())
					self.get_page().set_saved(False)
				else:
					#restore the current state
					n = self.get_page().get_state_cache().get_current_state()
					self.get_flow_graph().import_data(n)
					self.get_flow_graph().update()
		##################################################
		# Undo/Redo
		##################################################
		elif action == Actions.FLOW_GRAPH_UNDO:
			n = self.get_page().get_state_cache().get_prev_state()
			if n:
				self.get_flow_graph().unselect()
				self.get_flow_graph().import_data(n)
				self.get_flow_graph().update()
				self.get_page().set_saved(False)
		elif action == Actions.FLOW_GRAPH_REDO:
			n = self.get_page().get_state_cache().get_next_state()
			if n:
				self.get_flow_graph().unselect()
				self.get_flow_graph().import_data(n)
				self.get_flow_graph().update()
				self.get_page().set_saved(False)
		##################################################
		# New/Open/Save/Close
		##################################################
		elif action == Actions.FLOW_GRAPH_NEW:
			self.main_window.new_page()
		elif action == Actions.FLOW_GRAPH_OPEN:
			file_paths = OpenFlowGraphFileDialog(self.get_page().get_file_path()).run()
			if file_paths: #open a new page for each file, show only the first
				for i,file_path in enumerate(file_paths):
					self.main_window.new_page(file_path, show=(i==0))
		elif action == Actions.FLOW_GRAPH_CLOSE:
			self.main_window.close_page()
		elif action == Actions.FLOW_GRAPH_SAVE:
			#read-only or undefined file path, do save-as
			if self.get_page().get_read_only() or not self.get_page().get_file_path():
				Actions.FLOW_GRAPH_SAVE_AS()
			#otherwise try to save
			else:
				try:
					ParseXML.to_file(self.get_flow_graph().export_data(), self.get_page().get_file_path())
					self.get_page().set_saved(True)
				except IOError:
					Messages.send_fail_save(self.get_page().get_file_path())
					self.get_page().set_saved(False)
		elif action == Actions.FLOW_GRAPH_SAVE_AS:
			file_path = SaveFlowGraphFileDialog(self.get_page().get_file_path()).run()
			if file_path is not None:
				self.get_page().set_file_path(file_path)
				Actions.FLOW_GRAPH_SAVE()
		elif action == Actions.FLOW_GRAPH_SCREEN_CAPTURE:
			file_path = SaveImageFileDialog(self.get_page().get_file_path()).run()
			if file_path is not None:
				pixbuf = self.get_flow_graph().get_drawing_area().get_pixbuf()
				pixbuf.save(file_path, IMAGE_FILE_EXTENSION[1:])
		##################################################
		# Gen/Exec/Stop
		##################################################
		elif action == Actions.FLOW_GRAPH_GEN:
			if not self.get_page().get_proc():
				if not self.get_page().get_saved() or not self.get_page().get_file_path():
					Actions.FLOW_GRAPH_SAVE() #only save if file path missing or not saved
				if self.get_page().get_saved() and self.get_page().get_file_path():
					generator = self.get_page().get_generator()
					try:
						Messages.send_start_gen(generator.get_file_path())
						generator.write()
					except Exception,e: Messages.send_fail_gen(e)
				else: self.generator = None
		elif action == Actions.FLOW_GRAPH_EXEC:
			if not self.get_page().get_proc():
				Actions.FLOW_GRAPH_GEN()
				if self.get_page().get_saved() and self.get_page().get_file_path():
					ExecFlowGraphThread(self)
		elif action == Actions.FLOW_GRAPH_KILL:
			if self.get_page().get_proc():
				try: self.get_page().get_proc().kill()
				except: print "could not kill process: %d"%self.get_page().get_proc().pid
		elif action == Actions.PAGE_CHANGE: #pass and run the global actions
			pass
		else: print '!!! Action "%s" not handled !!!'%action
		##################################################
		# Global Actions for all States
		##################################################
		#update general buttons
		Actions.ERRORS_WINDOW_DISPLAY.set_sensitive(not self.get_flow_graph().is_valid())
		Actions.ELEMENT_DELETE.set_sensitive(bool(self.get_flow_graph().get_selected_elements()))
		Actions.BLOCK_PARAM_MODIFY.set_sensitive(bool(self.get_flow_graph().get_selected_block()))
		Actions.BLOCK_ROTATE_CCW.set_sensitive(bool(self.get_flow_graph().get_selected_blocks()))
		Actions.BLOCK_ROTATE_CW.set_sensitive(bool(self.get_flow_graph().get_selected_blocks()))
		#update cut/copy/paste
		Actions.BLOCK_CUT.set_sensitive(bool(self.get_flow_graph().get_selected_blocks()))
		Actions.BLOCK_COPY.set_sensitive(bool(self.get_flow_graph().get_selected_blocks()))
		Actions.BLOCK_PASTE.set_sensitive(bool(self.clipboard))
		#update enable/disable
		Actions.BLOCK_ENABLE.set_sensitive(bool(self.get_flow_graph().get_selected_blocks()))
		Actions.BLOCK_DISABLE.set_sensitive(bool(self.get_flow_graph().get_selected_blocks()))
		#set the exec and stop buttons
		self.update_exec_stop()
		#saved status
		Actions.FLOW_GRAPH_SAVE.set_sensitive(not self.get_page().get_saved())
		self.main_window.update()
		try: #set the size of the flow graph area (if changed)
			new_size = self.get_flow_graph().get_option('window_size')
			if self.get_flow_graph().get_size() != tuple(new_size):
				self.get_flow_graph().set_size(*new_size)
		except: pass
		#draw the flow graph
		self.get_flow_graph().update_selected()
		self.get_flow_graph().queue_draw()
		return True #action was handled

	def update_exec_stop(self):
		"""
		Update the exec and stop buttons.
		Lock and unlock the mutex for race conditions with exec flow graph threads.
		"""
		sensitive = self.get_flow_graph().is_valid() and not self.get_page().get_proc()
		Actions.FLOW_GRAPH_GEN.set_sensitive(sensitive)
		Actions.FLOW_GRAPH_EXEC.set_sensitive(sensitive)
		Actions.FLOW_GRAPH_KILL.set_sensitive(self.get_page().get_proc() != None)

class ExecFlowGraphThread(Thread):
	"""Execute the flow graph as a new process and wait on it to finish."""

	def __init__ (self, action_handler):
		"""
		ExecFlowGraphThread constructor.
		@param action_handler an instance of an ActionHandler
		"""
		Thread.__init__(self)
		self.update_exec_stop = action_handler.update_exec_stop
		self.flow_graph = action_handler.get_flow_graph()
		#store page and dont use main window calls in run
		self.page = action_handler.get_page()
		Messages.send_start_exec(self.page.get_generator().get_file_path())
		#get the popen
		try:
			self.p = self.page.get_generator().get_popen()
			self.page.set_proc(self.p)
			#update
			self.update_exec_stop()
			self.start()
		except Exception, e:
			Messages.send_verbose_exec(str(e))
			Messages.send_end_exec()

	def run(self):
		"""
		Wait on the executing process by reading from its stdout.
		Use gobject.idle_add when calling functions that modify gtk objects.
		"""
		#handle completion
		r = "\n"
		while(r):
			gobject.idle_add(Messages.send_verbose_exec, r)
			r = os.read(self.p.stdout.fileno(), 1024)
		gobject.idle_add(self.done)

	def done(self):
		"""Perform end of execution tasks."""
		Messages.send_end_exec()
		self.page.set_proc(None)
		self.update_exec_stop()
