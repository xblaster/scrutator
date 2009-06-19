import ihooks

class MyImportHook(ihooks.ModuleImporter):
    def import_module(self, name, globals=None, locals=None, fromlist=None):
        return ihooks.ModuleImporter.import_module(self, name, globals, locals, fromlist)

print 'Installed import hook'
MyImportHook().install()

import sys

