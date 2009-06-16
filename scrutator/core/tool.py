# -*- coding: utf-8 -*-
import sys
import time


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
			print "try loading "+packageName
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


	      #smart_load('scrutator.core.sync.event.FileRequest')
	      from scrutator.core.sync.event import FileRequest
	      event = FileRequest(file=file_check)
	      bus.push(event)
	      

	  

#try to import the file
def __try_import(packageName, retry = 10):
	#print "try left "+str(retry)+" for package "+str(packageName)
	if retry ==0:
		raise Exception("Retry exceed for smart_load import of '"+packageName+"'")
	try:
	 	imp = __import__(packageName, globals())	
	except ImportError:
		bus = get_smart_load_bus()
		#if we have a smart_load bus we try to fetch the file
		if bus:
			__check_tree(packageName)
			import scrutator.core.sync.event
			event = scrutator.core.sync.event.FileRequest(file=(packageName.replace('.','/')+'.py'))
			print "push "+str(event)+' to '+str(bus)
			bus.push(event)
			
		from twisted.internet import reactor
		import time
		
		reactor.iterate(10)
		time.sleep(1)
		#try to reimport it with a retry less
		return __try_import(packageName, retry -1)
	return imp
