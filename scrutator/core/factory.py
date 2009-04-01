from scrutator.core.tool import *
from scrutator.core.manager  import *

class XMLBeanConstArgError(Exception):
	pass

def getText(nodelist):
    rc = ""
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc = rc + node.data
    return rc


class AbstractBeanFactory:

	def __init__(self):
		pass
	

class XMLBeanFactory(AbstractBeanFactory):
	def __init__(self, resource):
		
		
		from xml.dom.minidom import parse
		from sys import path
		resource_name = path[0]+'/'+resource
		#print resource_name
		doc = parse(resource_name)
		for bean in doc.getElementsByTagName('bean'):
			self.loadBean(bean)
	
	def loadBean(self, bean):
		"""load a bean"""
		bean_id  = bean.getAttribute('id')
		class_name = bean.getAttribute('class')
		
		argument_list = list()
		
		#fetch element in constructor arg
		args = bean.getElementsByTagName('constructor-arg')
		
		#if we have params for constructor
		if len(args) == 1:
			arg = args[0]
			for node in arg.childNodes:
				
				#fetch value
				if (node.nodeName == "value"):
					val = getText(node.childNodes)
					
					#if value is an int, convert it
					if val.isdigit():
						val = int(val)
						
					#append element to argument list
					argument_list.append(val)
				
				#if we have reference element, fetch it with the getBean method
				#warning: you must declare reference before using it
				if (node.nodeName == "ref"):
					argument_list.append(CoreManager().getBean(node.getAttribute("bean")))
		
		#smart load reference of the class			
		class_obj = smart_load(class_name)
		try:
			if (len(argument_list)==0):
				class_inst = class_obj()
			else:
				class_inst = class_obj(*argument_list)
		except TypeError, e:
			raise XMLBeanConstArgError(class_obj.__name__+" bad args "+str(argument_list)+"\n"+str(e))
		
		#affect properties
		for property in bean.getElementsByTagName('property'):
			if len(property.getElementsByTagName('value')) > 0:
				value = getText(property.getElementsByTagName('value')[0].childNodes)
				setattr(class_inst, property.getAttribute('name'), value)
			else: 
				value = property.getElementsByTagName('ref')[0].getAttribute('bean')
				bean_class = CoreManager().getBean(value)
				setattr(class_inst, property.getAttribute('name'), bean_class)
		CoreManager().setBean(bean_id, class_inst)
			