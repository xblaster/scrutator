import scrutator.core.event

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
		basePath = globals()
		obj_new_root = basePath[sourceTree.pop(0)]
	else:
		obj_new_root = getattr(basePath, sourceTree.pop(0))
	
	recusSearch = __fetch_object(objectSourceTree, obj_new_root)
	if recusSearch == None:
		return obj_new_root
	else:
		return recusSearch

def __safeimport(packageName):
	#to implement
	pass