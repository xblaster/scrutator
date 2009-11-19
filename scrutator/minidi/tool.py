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
	
def __fetch_object(objectSourceTree, basePath=None):
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
			raise SmartLoadError("Can't import '" + str(basePath) + '.' + popelt + "'")
	
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
	try:
		log.msg("EXEC "+packageName)
		exec(packageName)
		#print "REPLICATE"
	except (NameError),e:
		log.msg(str(e))
		"""this is a not so safe import for the moment"""
		global __safeimport_dict
		log.msg("safe import " +str(__safeimport_dict))
		
		if not packageName in __safeimport_dict:
			log.msg("__safeimport " + packageName)
			__safeimport_dict[packageName] = __try_import(packageName)
		
		#put packageName in global
		globals()[packageName] = __safeimport_dict[packageName]
		log.msg("IMPORTED !!!"+str(__safeimport_dict))
		return __safeimport_dict[packageName]


def __check_tree(packageName):
      arbo = packageName.split('.')

      #remove last entry
      arbo.pop()

      import os

      while len(arbo) != 0:
	  file_check = str.join('/', arbo) + '/__init__.py'
	  arbo.pop()
	  
	  #if __init does not exist, we fetch it
	  log.msg("check " + str(file_check))
	  if not os.path.isfile(file_check):
	      bus = get_smart_load_bus()
	      from scrutator.core.sync.event import FileRequest
	      event = FileRequest(file=file_check)
	      log.msg("Launch async4 call for " + str(packageName))
	      log.msg("push " + str(event) + ' to ' + str(bus))
	      bus.push(event)
	      #from twisted.internet import reactor
	      #reactor.iterate()

def packagename_to_packagefile(packageName):
	return (packageName.replace('.', '/') + '.py')
	  
#asynchronously import a file
def __async_import(packageName):
	bus = get_smart_load_bus()
	#if we have a smart_load bus we try to fetch the file
	if bus:
		__check_tree(packageName)
		import scrutator.core.sync.event
		event = scrutator.core.sync.event.FileRequest(file=packagename_to_packagefile(packageName))
		log.msg("Launch async call for " + str(packageName))
		log.msg("push " + str(event) + ' to ' + str(bus))
		bus.push(event)
	else:
		raise Exception("no distant bus")
		

#try to import the file
def __try_import(packageName):
	#log.msg("try left "+str(retry)+" for package "+str(packageName))
	imp = None
	async_call = False
	
	while imp == None:
		packageFile = packagename_to_packagefile(packageName)
		
		#log.msg("Loop")
		#if source file does not exist
		log.msg("package file "+packageFile)
		if not (os.path.isfile('upload/' + packageFile) or os.path.isfile(packageFile)):
			#require it at first call
			if not async_call:
				threads.deferToThread(__async_import, packageName)
				async_call = True
			reactor.iterate(4)
		else:
			imp = __import__(packageName)	
			log.msg("IMP "+str(imp))
			try:
				log.msg("try importing")
				#imp = __import__(packageName)	
			except (Exception), exp:
				log.msg(str(exp))
				log.msg("Error during import")
				return None
			log.msg(imp)
		
		

		#try to reimport it with a retry less
	log.msg("Return __try_import "+str(imp))
	return imp
