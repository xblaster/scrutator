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
		doc = parse(resource)
		for bean in doc.getElementsByTagName('bean'):
			self.loadBean(bean)
	
	def loadBean(self, bean):
		bean_id  = bean.getAttribute('id')
		class_name = bean.getAttribute('class')
		
		argument_list = list()
		
		args = bean.getElementsByTagName('constructor-arg')
		if len(args) == 1:
			arg = args[0]
			for node in arg.childNodes:
				if (node.nodeName == "value"):
					val = getText(node.childNodes)
					if val.isdigit():
						val = int(val)
					argument_list.append(val)
				if (node.nodeName == "ref"):
					argument_list.append(CoreManager().getBean(node.getAttribute("bean")))
					
		class_obj = smart_load(class_name)
		try:
			if (len(argument_list)==0):
				class_inst = class_obj()
			else:
				class_inst = class_obj(argument_list)
		except TypeError:
			raise XMLBeanConstArgError(class_obj.__name__+" bad args "+str(argument_list)+"\n")
		
		for property in bean.getElementsByTagName('property'):
			if len(property.getElementsByTagName('value')) > 0:
				value = getText(property.getElementsByTagName('value')[0].childNodes)
				setattr(class_inst, property.getAttribute('name'), value)
			else: 
				value = property.getElementsByTagName('ref')[0].getAttribute('bean')
				bean_class = CoreManager().getBean(value)
				setattr(class_inst, property.getAttribute('name'), bean_class)
		CoreManager().setBean(bean_id, class_inst)
			