# -*- coding: utf-8 -*-
import sys, time, os

from twisted.internet import threads, reactor
from twisted.python import log

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
			log.msg("__safeimport "+packageName)
			__safeimport_dict[packageName] = __try_import(packageName)
		
		#put packageName in global
		globals()[packageName] = __safeimport_dict[packageName]
		return __safeimport_dict[packageName]
		#exec("global "+packageName.split('.').pop(0))
			
		#print "---------"
		#print globals()
		#for v in globals():
			#print str(v)


def __check_tree(packageName):
      arbo = packageName.split('.')

      #remove last entry
      arbo.pop()

      import os

      while len(arbo) !=0:
	  file_check = str.join('/',arbo)+'/__init__.py'
	  arbo.pop()
	  
	  #if __init does not exist, we fetch it
	  print "check "+str(file_check)
	  if not os.path.isfile(file_check):
	      bus = get_smart_load_bus()
	      from scrutator.core.sync.event import FileRequest
	      event = FileRequest(file=file_check)
	      log.msg("Launch async call for "+str(packageName))
	      bus.push(event)
	      #from twisted.internet import reactor
	      #reactor.iterate()

def packagename_to_packagefile(packageName):
	return (packageName.replace('.','/')+'.py')
	  
#asynchronously import a file
def __async_import(packageName):
	bus = get_smart_load_bus()
	#if we have a smart_load bus we try to fetch the file
	if bus:
		__check_tree(packageName)
		import scrutator.core.sync.event
		event = scrutator.core.sync.event.FileRequest(file=packagename_to_packagefile(packageName))
		print "push "+str(event)+' to '+str(bus)
		bus.push(event)

#try to import the file
def __try_import(packageName):
	#print "try left "+str(retry)+" for package "+str(packageName)		
	imp = None
	async_call = False
	
	while imp == None:
		packageFile = packagename_to_packagefile(packageName)
		#log.msg("Loop")
				
		#if source file does not exist
		if not (os.path.isfile('upload/'+packageFile) or os.path.isfile(packageFile)):
			#require it at first call
			if not async_call:
				log.msg("Launch async call for "+str(packageName))
				threads.deferToThread(__async_import, packageName)
				async_call = True
			reactor.iterate(4)
		else:
			try:
				imp = __import__(packageName)
			except ImportError:
				log.err()
				return None
			
		

		#try to reimport it with a retry less
		#return __try_import(packageName, retry -1)
	return imp
