# -*- coding: utf-8 -*-
#remove upload dir
import shutil
shutil.rmtree('upload', True)
from scrutator.core.tool import *


#install hook
import ihooks

class SyncHook(ihooks.ModuleImporter):
    def import_module(self, name, globals=None, locals=None, fromlist=None, level= -1):
		try:
			imp = ihooks.ModuleImporter.import_module(self, name, globals, locals, fromlist)
		except:
			smart_import(name)
			imp = ihooks.ModuleImporter.import_module(self, name, globals, locals, fromlist)
		return imp
		



print 'Install sync_hook'
SyncHook().install()
