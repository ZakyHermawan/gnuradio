#
# Copyright 2008 Free Software Foundation, Inc.
#
# This file is part of GNU Radio
#
# GNU Radio is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# GNU Radio is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GNU Radio; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
#

import wx

def bind_to_visible_event(win, callback):
	"""
	Bind a callback to a window when its visibility changes.
	Specifically, callback when the window changes visibility
	when a notebook tab event in one of the parents occurs.
	@param win the wx window
	@param callback a 1 param function
	"""
	#is the window visible in the hierarchy
	def is_wx_window_visible(my_win):
		while True:
			parent = my_win.GetParent()
			if not parent: return True #reached the top of the hierarchy
			#if we are hidden, then finish, otherwise keep traversing up
			if isinstance(parent, wx.Notebook) and parent.GetCurrentPage() != my_win: return False
			my_win = parent
	#call the callback, the arg is shown or not
	def callback_factory(my_win, my_callback):
		cache = [None]
		def the_callback(*args):
			visible = is_wx_window_visible(my_win)
			if cache[0] != visible: my_callback(visible)
			cache[0] = visible
		return the_callback
	handler = callback_factory(win, callback)
	#bind the handler to all the parent notebooks
	while win:
		if isinstance(win, wx.Notebook):
			win.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, handler)
		if not win.GetParent():
			win.Bind(wx.EVT_ACTIVATE, handler)
		win = win.GetParent()

#A macro to apply an index to a key
index_key = lambda key, i: "%s_%d"%(key, i+1)

def _register_access_method(destination, controller, key):
	"""
	Helper function for register access methods.
	This helper creates distinct set and get methods for each key
	and adds them to the destination object.
	"""
	def set(value): controller[key] = value
	setattr(destination, 'set_'+key, set)
	def get(): return controller[key]
	setattr(destination, 'get_'+key, get) 

def register_access_methods(destination, controller):
	"""
	Register setter and getter functions in the destination object for all keys in the controller.
	@param destination the object to get new setter and getter methods
	@param controller the pubsub controller
	"""
	for key in controller.keys(): _register_access_method(destination, controller, key)

##################################################
# Input Watcher Thread
##################################################
from gnuradio import gru

class input_watcher(gru.msgq_runner):
	"""
	Input watcher thread runs forever.
	Read messages from the message queue.
	Forward messages to the message handler.
	"""
	def __init__ (self, msgq, controller, msg_key, arg1_key='', arg2_key=''):
		self._controller = controller
		self._msg_key = msg_key
		self._arg1_key = arg1_key
		self._arg2_key = arg2_key
		gru.msgq_runner.__init__(self, msgq, self.handle_msg)

	def handle_msg(self, msg):
		if self._arg1_key: self._controller[self._arg1_key] = msg.arg1()
		if self._arg2_key: self._controller[self._arg2_key] = msg.arg2()
		self._controller[self._msg_key] = msg.to_string()


##################################################
# Shared Functions
##################################################
import numpy
import math

def get_exp(num):
	"""
	Get the exponent of the number in base 10.
	@param num the floating point number
	@return the exponent as an integer
	"""
	if num == 0: return 0
	return int(math.floor(math.log10(abs(num))))

def get_clean_num(num):
	"""
	Get the closest clean number match to num with bases 1, 2, 5.
	@param num the number
	@return the closest number
	"""
	if num == 0: return 0
	sign = num > 0 and 1 or -1
	exp = get_exp(num)
	nums = numpy.array((1, 2, 5, 10))*(10**exp)
	return sign*nums[numpy.argmin(numpy.abs(nums - abs(num)))]

def get_clean_incr(num):
	"""
	Get the next higher clean number with bases 1, 2, 5.
	@param num the number
	@return the next higher number
	"""
	num = get_clean_num(num)
	exp = get_exp(num)
	coeff = int(round(num/10**exp))
	return {
		-5: -2,
		-2: -1,
		-1: -.5,
		1: 2,
		2: 5,
		5: 10,
	}[coeff]*(10**exp)

def get_clean_decr(num):
	"""
	Get the next lower clean number with bases 1, 2, 5.
	@param num the number
	@return the next lower number
	"""
	num = get_clean_num(num)
	exp = get_exp(num)
	coeff = int(round(num/10**exp))
	return {
		-5: -10,
		-2: -5,
		-1: -2,
		1: .5,
		2: 1,
		5: 2,
	}[coeff]*(10**exp)

def get_min_max(samples):
	"""
	Get the minimum and maximum bounds for an array of samples.
	@param samples the array of real values
	@return a tuple of min, max
	"""
	scale_factor = 3
	mean = numpy.average(samples)
	rms = numpy.max([scale_factor*((numpy.sum((samples-mean)**2)/len(samples))**.5), .1])
	min_val = mean - rms
	max_val = mean + rms
	return min_val, max_val

def get_min_max_fft(fft_samps):
	"""
	Get the minimum and maximum bounds for an array of fft samples.
	@param samples the array of real values
	@return a tuple of min, max
	"""
	#get the peak level (max of the samples)
	peak_level = numpy.max(fft_samps)
	#separate noise samples
	noise_samps = numpy.sort(fft_samps)[:len(fft_samps)/2]
	#get the noise floor
	noise_floor = numpy.average(noise_samps)
	#get the noise deviation
	noise_dev = numpy.std(noise_samps)
	#determine the maximum and minimum levels
	max_level = peak_level
	min_level = noise_floor - abs(2*noise_dev)
	return min_level, max_level
