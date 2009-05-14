#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gobject
import gtk
from twisted.internet import threads, reactor
from scrutator.core.listener import *

class GtkDebugListener(SimpleListener):
	def __init__(self):
		self.debug_list = list()
		super(GtkDebugListener, self).__init__()
		
		self.window = GtkDebugWindow(None, self) 

		
	def action(self, eventObj, evtMgr):
		self.debug_list.insert(0,eventObj)
		self.window.onRefresh()
	
	def getDebugList(self):
		return self.debug_list

ui_info = \
'''<ui>
  <menubar name='MenuBar'>
	<menu action='FileMenu'>
	  <menuitem action='Quit'/>
	</menu>
  </menubar>
  <toolbar	name='ToolBar'>
	<toolitem action='Refresh'/>
	<toolitem action='Quit'/>
  </toolbar>
</ui>'''

def activate_action(action):
	print 'Action "%s" activated' % action.get_name()





class GtkDebugWindow(gtk.Window):



	def __init__(self, parent, listener):
		
		self.entries = (
		  ( "FileMenu", None, "_File" ),			   # name, stock id, label
		  ( "PreferencesMenu", None, "_Preferences" ), # name, stock id, label
		  ( "ColorMenu", None, "_Color"	 ),			   # name, stock id, label
		  ( "ShapeMenu", None, "_Shape" ),			   # name, stock id, label
		  ( "HelpMenu", None, "_Help" ),			   # name, stock id, label
		  ( "Refresh", gtk.STOCK_REFRESH,					  # name, stock id
			"_Refresh","<control>R",					  # label, accelerator
			"Refresh the list",								# tooltip
			self.onRefresh ),

		  ( "Quit", gtk.STOCK_QUIT,					   # name, stock id
			"_Quit", "<control>Q",					   # label, accelerator
			"Quit",									   # tooltip
			self.onClose )
		)
		
		#initiate GtkDebugListener
		self.listener = listener
		gtk.Window.__init__(self)
		
		self.set_default_size(640,480)
		
		try:
			self.set_screen(parent.get_screen())
		except AttributeError:
			self.connect('destroy', lambda *w: gtk.main_quit())
		self.set_title(self.__class__.__name__)
		self.set_border_width(0)

		actions = gtk.ActionGroup("Actions")
		actions.add_actions(self.entries)
		#actions.add_toggle_actions(toggle_entries)
		#actions.add_radio_actions(color_entries, COLOR_RED, activate_radio_action)
		#actions.add_radio_actions(shape_entries, SHAPE_OVAL, activate_radio_action)

		ui = gtk.UIManager()
		ui.insert_action_group(actions, 0)
		self.add_accel_group(ui.get_accel_group())
		
		try:
			mergeid = ui.add_ui_from_string(ui_info)
		except gobject.GError, msg:
			print "building menus failed: %s" % msg
			
		box1 = gtk.VBox(False, 0)
		self.add(box1)

		box1.pack_start(ui.get_widget("/MenuBar"), False, False, 0)
		box1.pack_start(ui.get_widget("/ToolBar"), False, False, 0)
		
		self.mainList = self.getMainList()
		scrolled_window = gtk.ScrolledWindow()
		scrolled_window.add_with_viewport(self.mainList)
		scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)


		
		box1.pack_start(scrolled_window, True, True)
		

		self.show_all()

		#reactor.callLater(0.5, self.onRefresh)

	def onClose(self,action):
		gtk.main_quit()

	def onRefresh(self,action = None):
		for child in self.mainList.get_children():
			self.mainList.remove(child)
		
		self.mainList.add(self.getMainList())
		self.show_all()
		#reactor.callLater(0.2, self.onRefresh)

	def getMainList(self):
		mainList = gtk.VBox(False,0)
		for i in self.listener.getDebugList():
			v = gtk.HBox(False,0)
			v.pack_start(gtk.Label(i.getString()),False,False)
			mainList.add(v)
		return mainList
		
