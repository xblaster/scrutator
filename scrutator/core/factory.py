from scrutator.core.tool import *
from scrutator.core.manager  import *

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
		
		class_inst = smart_load(class_name)()
		
		for property in bean.getElementsByTagName('property'):
			if len(property.getElementsByTagName('value')) > 0:
				value = getText(property.getElementsByTagName('value')[0].childNodes)
				setattr(class_inst, property.getAttribute('name'), value)
			else: 
				value = property.getElementsByTagName('ref')[0].getAttribute('bean')
				bean_class = CoreManager().getBean(value)
				setattr(class_inst, property.getAttribute('name'), bean_class)
		CoreManager().setBean(bean_id, class_inst)
			