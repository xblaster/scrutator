class AbstractBeanFactory:
	self.beans_list = dict()
	def __init__(self):
		pass
	
	def getBean(self, beanName):
		if self.beans_list.has_key(beanName):
			return self.beans_list[beanName]
		raise Exception('This bean does not exist')
	
	def setBean(self, beanName, beanObj):
		self.beans_list[beanName] = beanObj

class XMLBeanFactory(AbstractBeanFactory):
	def __init__(self, resource):
		