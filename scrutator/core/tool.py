# -*- coding: utf-8 -*-
import sys

def smart_load(classFullString):
	"""load automatically a class with this name (include package)"""
	xpld = str(classFullString).split('.')
	class_name = xpld.pop()
	
	#safe import scrit
	__safeimport(str('.').join(xpld))
	
	return __fetch_object(str(classFullString).split('.'))

class SmartLoadError(Exception):
	pass
	
def __fetch_object(objectSourceTree, basePath = None):
	sourceTree = objectSourceTree
	
	if len(sourceTree) == 0:
		return None
	
	if not basePath:
		obj_new_root = sys.modules[sourceTree.pop(0)] 
	else:
		popelt = sourceTree.pop(0)
		try:
			obj_new_root = getattr(basePath, popelt)
		except AttributeError:
			raise SmartLoadError("Can't import '"+ str(basePath)+'.'+popelt+"'")
	
	recusSearch = __fetch_object(objectSourceTree, obj_new_root)
	if recusSearch == None:
		return obj_new_root
	else:
		return recusSearch


__safeimport_dict = dict()

__smart_load_bus = None

def define_smart_load_bus(manager):
	global __smart_load_bus
	__smart_load_bus = manager

def get_smart_load_bus():
	global __smart_load_bus
	return __smart_load_bus

def smart_import(packageName):
	return __safeimport(packageName)

def __safeimport(packageName):
	"""this is a not so safe import for the moment"""
	try:
		exec(packageName)
		#print "REPLICATE"
	except NameError:
		
		global __safeimport_dict
		
		if not packageName in __safeimport_dict:
			print "load "+packageName
			__safeimport_dict[packageName] = __try_import(packageName)
		
		#put packageName in global
		globals()[packageName] = __safeimport_dict[packageName]
		return __safeimport_dict[packageName]
		#exec("global "+packageName.split('.').pop(0))
			
		#print "---------"
		#print globals()
		#for v in globals():
			#print str(v)

#try to import the file
def __try_import(packageName, retry = 10):
	if retry <= 0:
	    raise Exception("too many recursion for package "+str(packageName))
	try:
	 	imp = __import__(packageName, globals())	
	except ImportError:
		bus = get_smart_load_bus()
		#if we have a smart_load bus we try to fetch the file
		if bus:
			from scrutator.core.sync.event import *
			event = FileRequest(file=packageName)
			bus.push(event)
			
			from twisted.internet import reactor
			import time
			reactor.iterate(10)
			time.sleep(0.5)
		#try to reimport it with a retry less
		return __try_import(packageName, retry -1)
	return imp