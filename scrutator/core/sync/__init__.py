# -*- coding: utf-8 -*-
#remove upload dir
import shutil
shutil.rmtree('upload', True)
from scrutator.minidi.tool import *

import sys
sys.path.append('upload')

#install hook
import ihooks

#class SyncHook(ihooks.ModuleImporter):
#    def import_module(self, name, globals=None, locals=None, fromlist=None, level= -1):
#        try:
#            imp = ihooks.ModuleImporter.import_module(self, name, globals, locals, fromlist)
#        #except (NameError, ImportError) as e:
#        except:
#            try:
#                smart_import(name)
#                imp = ihooks.ModuleImporter.import_module(self, name, globals, locals, fromlist)
#            except (Exception), e:
#                log.msg("Error during smart_import" +str(e))
#                pass
#        return imp
class SyncHook(ihooks.ModuleImporter):
    def import_module(self, name, globals=None, locals=None, fromlist=None, level = -1):
        #smart_import(name)
        try:
            imp = ihooks.ModuleImporter.import_module(self, name, globals, locals, fromlist)
        except Exception:
            import traceback
            #traceback.print_exc(file=sys.stdout)
            smart_import(name)
            imp = ihooks.ModuleImporter.import_module(self, name, globals, locals, fromlist)
        return imp

print 'Install sync_hook'
SyncHook().install()
