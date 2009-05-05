#!/usr/bin/env python

import gobject
import gtk

ui_info = \
'''<ui>
  <menubar name='MenuBar'>
    <menu action='FileMenu'>
      <menuitem action='New'/>
      <menuitem action='Open'/>
      <menuitem action='Import'/>
      <menuitem action='Save'/>
      <menuitem action='SaveAs'/>
      <separator/>
      <menuitem action='Quit'/>
    </menu>
    <menu action='HelpMenu'>
      <menuitem action='About'/>
    </menu>
  </menubar>
  <toolbar  name='ToolBar'>
    <toolitem action='Open'/>
    <toolitem action='Quit'/>
    <separator action='Sep1'/>
    <toolitem action='Logo'/>
  </toolbar>
</ui>'''

def activate_action(action):
    print 'Action "%s" activated' % action.get_name()

entries = (
  ( "FileMenu", None, "_File" ),               # name, stock id, label
  ( "PreferencesMenu", None, "_Preferences" ), # name, stock id, label
  ( "ColorMenu", None, "_Color"  ),            # name, stock id, label
  ( "ShapeMenu", None, "_Shape" ),             # name, stock id, label
  ( "HelpMenu", None, "_Help" ),               # name, stock id, label
  ( "New", gtk.STOCK_NEW,                      # name, stock id
    "_New", "<control>N",                      # label, accelerator
    "Create a new file",                       # tooltip
    activate_action ),
  ( "Open", gtk.STOCK_OPEN,                    # name, stock id
    "_Open","<control>O",                      # label, accelerator
    "Open a file",                             # tooltip
    activate_action ),
    ( "Import", gtk.STOCK_OPEN,                    # name, stock id
    "_Import","<control>I",                      # label, accelerator
    "Import a CSV",                             # tooltip
    activate_action ),
  ( "Save", gtk.STOCK_SAVE,                    # name, stock id
    "_Save","<control>S",                      # label, accelerator
    "Save current file",                       # tooltip
    activate_action ),
  ( "SaveAs", gtk.STOCK_SAVE,                  # name, stock id
    "Save _As...", None,                       # label, accelerator
    "Save to a file",                          # tooltip
    activate_action ),
  ( "Quit", gtk.STOCK_QUIT,                    # name, stock id
    "_Quit", "<control>Q",                     # label, accelerator
    "Quit",                                    # tooltip
    activate_action ),
  ( "About", None,                             # name, stock id
    "_About", "<control>A",                    # label, accelerator
    "About",                                   # tooltip
    activate_action ),
  ( "Logo", "demo-gtk-logo",                   # name, stock id
     None, None,                               # label, accelerator
    "GTK+",                                    # tooltip
    activate_action ),
)

class MainWindow(gtk.Window):

    def __init__(self, parent=None):
        gtk.Window.__init__(self)
        try:
            self.set_screen(parent.get_screen())
        except AttributeError:
            self.connect('destroy', lambda *w: gtk.main_quit())
        self.set_title(self.__class__.__name__)
        self.set_border_width(0)

        actions = gtk.ActionGroup("Actions")
        actions.add_actions(entries)
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
        
        box1.pack_start(self.getMainList())
        
        self.show_all()
    
    def getMainList(self):
    	mainList = gtk.VBox(False,0)
    	for i in range(10):
    		pass
    	return mainList
    	

def main():
    MainWindow()
    gtk.main()

if __name__ == '__main__':
    main()