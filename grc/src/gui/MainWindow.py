"""
Copyright 2008 Free Software Foundation, Inc.
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

from Constants import \
	NEW_FLOGRAPH_TITLE, DEFAULT_REPORTS_WINDOW_WIDTH
from Actions import \
	APPLICATION_QUIT, FLOW_GRAPH_KILL, \
	FLOW_GRAPH_SAVE, get_accel_group
import pygtk
pygtk.require('2.0')
import gtk
import Bars
from BlockTreeWindow import BlockTreeWindow
from Dialogs import TextDisplay, MessageDialogHelper
from NotebookPage import NotebookPage
import Preferences
import Messages
import os

############################################################
# Main window
############################################################

class MainWindow(gtk.Window):
	"""The topmost window with menus, the tool bar, and other major windows."""

	def __init__(self, handle_states, platform):
		"""
		MainWindow contructor.
		@param handle_states the callback function
		"""
		self._platform = platform
		#setup window
		self.handle_states = handle_states
		gtk.Window.__init__(self, gtk.WINDOW_TOPLEVEL)
		vbox = gtk.VBox()
		self.hpaned = gtk.HPaned()
		self.add(vbox)
		#create the menu bar and toolbar
		self.add_accel_group(get_accel_group())
		vbox.pack_start(Bars.MenuBar(), False)
		vbox.pack_start(Bars.Toolbar(), False)
		vbox.pack_start(self.hpaned)
		#create the notebook
		self.notebook = gtk.Notebook()
		self.page_to_be_closed = None
		self.current_page = None
		self.notebook.set_show_border(False)
		self.notebook.set_scrollable(True) #scroll arrows for page tabs
		self.notebook.connect('switch-page', self._handle_page_change)
		#setup containers
		self.flow_graph_vpaned = gtk.VPaned()
		#flow_graph_box.pack_start(self.scrolled_window)
		self.flow_graph_vpaned.pack1(self.notebook)
		self.hpaned.pack1(self.flow_graph_vpaned)
		self.hpaned.pack2(BlockTreeWindow(platform, self.get_flow_graph), False) #dont allow resize
		#create the reports window
		self.text_display = TextDisplay()
		#house the reports in a scrolled window
		self.reports_scrolled_window = gtk.ScrolledWindow()
		self.reports_scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		self.reports_scrolled_window.add_with_viewport(self.text_display)
		self.reports_scrolled_window.set_size_request(-1, DEFAULT_REPORTS_WINDOW_WIDTH)
		self.flow_graph_vpaned.pack2(self.reports_scrolled_window, False) #dont allow resize
		#load preferences and show the main window
		Preferences.load(platform)
		self.resize(*Preferences.main_window_size())
		self.flow_graph_vpaned.set_position(Preferences.reports_window_position())
		self.hpaned.set_position(Preferences.blocks_window_position())
		self.show_all()

	############################################################
	# Event Handlers
	############################################################

	def _quit(self, window, event):
		"""
		Handle the delete event from the main window.
		Generated by pressing X to close, alt+f4, or right click+close.
		This method in turns calls the state handler to quit.
		@return true
		"""
		self.handle_states(APPLICATION_QUIT)
		return True

	def _handle_page_change(self, notebook, page, page_num):
		"""
		Handle a page change. When the user clicks on a new tab,
		reload the flow graph to update the vars window and
		call handle states (select nothing) to update the buttons.
		@param notebook the notebook
		@param page new page
		@param page_num new page number
		"""
		self.current_page = self.notebook.get_nth_page(page_num)
		Messages.send_page_switch(self.current_page.get_file_path())
		self.handle_states()

	############################################################
	# Report Window
	############################################################

	def add_report_line(self, line):
		"""
		Place line at the end of the text buffer, then scroll its window all the way down.
		@param line the new text
		"""
		self.text_display.insert(line)
		vadj = self.reports_scrolled_window.get_vadjustment()
		vadj.set_value(vadj.upper)
		vadj.emit('changed')

	############################################################
	# Pages: create and close
	############################################################

	def new_page(self, file_path='', show=False):
		"""
		Create a new notebook page.
		Set the tab to be selected.
		@param file_path optional file to load into the flow graph
		@param show true if the page should be shown after loading
		"""
		#if the file is already open, show the open page and return
		if file_path and file_path in self._get_files(): #already open
			page = self.notebook.get_nth_page(self._get_files().index(file_path))
			self._set_page(page)
			return
		try: #try to load from file
			if file_path: Messages.send_start_load(file_path)
			flow_graph = self._platform.get_new_flow_graph()
			page = NotebookPage(
				self,
				flow_graph=flow_graph,
				file_path=file_path,
			)
			if file_path: Messages.send_end_load()
		except Exception, e: #return on failure
			Messages.send_fail_load(e)
			return
		#add this page to the notebook
		self.notebook.append_page(page, page.get_tab())
		try: self.notebook.set_tab_reorderable(page, True)
		except: pass #gtk too old
		self.notebook.set_tab_label_packing(page, False, False, gtk.PACK_START)
		#only show if blank or manual
		if not file_path or show: self._set_page(page)

	def close_pages(self):
		"""
		Close all the pages in this notebook.
		@return true if all closed
		"""
		open_files = filter(lambda file: file, self._get_files()) #filter blank files
		open_file = self.get_page().get_file_path()
		#close each page
		for page in self._get_pages():
			self.page_to_be_closed = page
			self.close_page(False)
		if self.notebook.get_n_pages(): return False
		#save state before closing
		Preferences.files_open(open_files)
		Preferences.file_open(open_file)
		Preferences.main_window_size(self.get_size())
		Preferences.reports_window_position(self.flow_graph_vpaned.get_position())
		Preferences.blocks_window_position(self.hpaned.get_position())
		Preferences.save()
		return True

	def close_page(self, ensure=True):
		"""
		Close the current page.
		If the notebook becomes empty, and ensure is true,
		call new page upon exit to ensure that at least one page exists.
		@param ensure boolean
		"""
		if not self.page_to_be_closed: self.page_to_be_closed = self.get_page()
		#show the page if it has an executing flow graph or is unsaved
		if self.page_to_be_closed.get_pid() or not self.page_to_be_closed.get_saved():
			self._set_page(self.page_to_be_closed)
		#unsaved? ask the user
		if not self.page_to_be_closed.get_saved() and self._save_changes():
			self.handle_states(FLOW_GRAPH_SAVE) #try to save
			if not self.page_to_be_closed.get_saved(): #still unsaved?
				self.page_to_be_closed = None #set the page to be closed back to None
				return
		#stop the flow graph if executing
		if self.page_to_be_closed.get_pid(): self.handle_states(FLOW_GRAPH_KILL)
		#remove the page
		self.notebook.remove_page(self.notebook.page_num(self.page_to_be_closed))
		if ensure and self.notebook.get_n_pages() == 0: self.new_page() #no pages, make a new one
		self.page_to_be_closed = None #set the page to be closed back to None

	############################################################
	# Misc
	############################################################

	def update(self):
		"""
		Set the title of the main window.
		Set the titles on the page tabs.
		Show/hide the reports window.
		@param title the window title
		"""
		title = ''.join((
				self._platform.get_name(),
				' - Editing: ',
				(self.get_page().get_file_path() or NEW_FLOGRAPH_TITLE),
				(self.get_page().get_saved() and ' ' or '*'), #blank must be non empty
				(self.get_page().get_read_only() and ' (read-only)' or ''),
			)
		)
		gtk.Window.set_title(self, title)
		#set tab titles
		for page in self._get_pages():
			#get filename and strip out file extension
			title = os.path.splitext(os.path.basename(page.get_file_path()))[0]
			page.set_text(''.join((
						(title or NEW_FLOGRAPH_TITLE),
						(page.get_saved() and ' ' or '*'), #blank must be non empty
						(page.get_read_only() and ' (ro)' or ''),
					)
				)
			)
		#show/hide notebook tabs
		self.notebook.set_show_tabs(len(self._get_pages()) > 1)

	def get_page(self):
		"""
		Get the selected page.
		@return the selected page
		"""
		return self.current_page

	def get_flow_graph(self):
		"""
		Get the selected flow graph.
		@return the selected flow graph
		"""
		return self.get_page().get_flow_graph()

	def get_focus_flag(self):
		"""
		Get the focus flag from the current page.
		@return the focus flag
		"""
		return self.get_page().get_drawing_area().get_focus_flag()

	############################################################
	# Helpers
	############################################################

	def _set_page(self, page):
		"""
		Set the current page.
		@param page the page widget
		"""
		self.current_page = page
		self.notebook.set_current_page(self.notebook.page_num(self.current_page))

	def _save_changes(self):
		"""
		Save changes to flow graph?
		@return true if yes
		"""
		return MessageDialogHelper(
			gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO, 'Unsaved Changes!',
			'Would you like to save changes before closing?'
		) == gtk.RESPONSE_YES

	def _get_files(self):
		"""
		Get the file names for all the pages, in order.
		@return list of file paths
		"""
		return map(lambda page: page.get_file_path(), self._get_pages())

	def _get_pages(self):
		"""
		Get a list of all pages in the notebook.
		@return list of pages
		"""
		return [self.notebook.get_nth_page(page_num) for page_num in range(self.notebook.get_n_pages())]
