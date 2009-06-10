import sys

def smart_load(classFullString):
	"""load automatically a class with this name (include package)"""
	xpld = str(classFullString).split('.')
	class_name = xpld.pop()
	
	#safe import scrit
	__safeimport(str('.').join(xpld))
	
	return __fetch_object(str(classFullString).split('.'))
	
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
			raise Exception("Can't import '"+ str(basePath)+'.'+popelt+"'")
	
	recusSearch = __fetch_object(objectSourceTree, obj_new_root)
	if recusSearch == None:
		return obj_new_root
	else:
		return recusSearch


__safeimport_dict = dict()

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
			__safeimport_dict[packageName] = __import__(packageName, globals())
		
		globals()[packageName] = __safeimport_dict[packageName]
		return __safeimport_dict[packageName]
		#exec("global "+packageName.split('.').pop(0))
			
		#print "---------"
		#print globals()
		#for v in globals():
			#print str(v)
		