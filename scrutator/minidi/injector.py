'''
Created on 12 Nov 2009

@author: wax
'''

from scrutator.minidi.tool import smart_load

class ContextNotFoundException(Exception):
    pass


class Config(object):
    def __init__(self):
        self.context = None

    def load(self, context):
        self.context = context
        
    def hasObject(self, objectName):
        return False
    
    def getContext(self):
        return self.context

class XMLConfig(Config):
    def __init__(self, xml_filename):
        super(XMLConfig, self).__init__()
        self.filename = xml_filename
        
    def load(self,context):
        super(XMLConfig, self).load(context)
        XMLBeanFactory(self.filename, context)
        
class PythonConfig(Config):
    def __init__(self):
        super(PythonConfig, self).__init__()
        pass
    
    def hasObject(self, objectName):
        if objectName in dir(self):
            return True
        return False
    
    def loadObject(self, objectName, context):
        func = getattr(self, objectName)
        return func() 
    
class Context:
    """ default contexte interface """
    def __init__(self, *args):
        self.beans_list = dict()
        self.config_list = list()
        
        for config in args:
            if isinstance(config, Config):
                self.addConfig(config)
        
    def getBean(self, beanName):
        if self.hasObject(beanName):
            return self.beans_list[beanName]
        raise ContextNotFoundException('bean ' + str(beanName) + ' does not exist')

    def __ImplantGetContext(self):
        return self

    def setBean(self, beanName, beanObj):
        self.beans_list[beanName] = beanObj
        if not 'context' in dir(beanObj):
            #if no attribute name "context", we add the context
            beanObj.context = self 
            beanObj.getContext = self.__ImplantGetContext
        
    def get_object(self, object_name):
        """aliases for getBean"""
        return self.getBean(object_name)
    
    def getObject(self, object_name):
        """aliases for getBean"""
        return self.getBean(object_name)
    
    def hasObject(self, objectName):
        if self.beans_list.has_key(objectName):
            return True
        
        for config in self.config_list:
            if config.hasObject(objectName):
                #put object in beans_list
                self.beans_list[objectName] = config.loadObject(objectName, self)
                return True
            
        return False

    def addConfig(self, config):
        """
        add configuration to a context
        """
        if not isinstance(config, Config):
            raise Exception("Not a config object")
        
        config.load(self)
        self.config_list.append(config)
    

class CoreManager:
    """ A python singleton """

    class __CoreManagerimpl(Context):
        """ Implementation of the singleton interface """
        
        from scrutator.core.manager import EventManager 
        eventManager = EventManager()
        
        
        def push(self, eventObj):
            return self.eventManager.push(eventObj)
            
        


    # storage for the instance reference
    __instance = None

    def __init__(self):
        """ Create singleton instance """
        # Check whether we already have an instance
        if CoreManager.__instance is None:
            # Create and remember instance
            CoreManager.__instance = CoreManager.__CoreManagerimpl()
        
        # Store instance reference as the only member in the handle
        self.__dict__['_Singleton__instance'] = CoreManager.__instance

    def __getattr__(self, attr):
        """ Delegate access to implementation """
        return getattr(self.__instance, attr)
    
    def __setattr__(self, attr, value):
        """ Delegate access to implementation """
        return setattr(self.__instance, attr, value)



class XmlEventManagerLoader:
    
    def getListener(self, xmlNode, context):
        if xmlNode.hasAttribute('listener'):
            listenerName = xmlNode.getAttribute('listener')
            listenerClass = smart_load(listenerName)()
            return listenerClass
            
        if xmlNode.hasAttribute('bean'):
            beanName = xmlNode.getAttribute('bean')
            listenerClass = context.getBean(beanName)
            return listenerClass
        raise Exception('listener or bean')

    
    def load(self, filename, eventManager, context = CoreManager()):
        from xml.dom.minidom import parse
        from sys import path
        resource_name = path[0] + '/' + filename
        
        doc = parse(resource_name)
        
        for trigger in doc.getElementsByTagName('trigger'):
            eventName = trigger.getAttribute('event')

            
            #if it's not "all" events
            if not eventName == 'all':
                eventName = smart_load(eventName)().getType()
            
            
            eventManager.bind(eventName, self.getListener(trigger, context))
            

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
    def __init__(self, resource, context = CoreManager()):
        
        self.context = context
        
        from xml.dom.minidom import parse
        from sys import path
        resource_name = path[0] + '/' + resource
        doc = parse(resource_name)
        for bean in doc.getElementsByTagName('bean'):
            self.loadBean(bean)
    
    def loadBean(self, bean):
        """load a bean"""
        bean_id = bean.getAttribute('id')
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
                    argument_list.append(self.context.getBean(node.getAttribute("bean")))
        
        #smart load reference of the class            
        class_obj = smart_load(class_name)
        try:
            if (len(argument_list) == 0):
                class_inst = class_obj()
            else:
                class_inst = class_obj(*argument_list)
        except TypeError, e:
            raise XMLBeanConstArgError(class_obj.__name__ + " bad args " + str(argument_list) + "\n" + str(e))
        
        #affect properties
        for property in bean.getElementsByTagName('property'):
            if len(property.getElementsByTagName('value')) > 0:
                value = getText(property.getElementsByTagName('value')[0].childNodes)
                setattr(class_inst, property.getAttribute('name'), value)
            else: 
                value = property.getElementsByTagName('ref')[0].getAttribute('bean')
                bean_class = self.context.getBean(value)
                setattr(class_inst, property.getAttribute('name'), bean_class)
        self.context.setBean(bean_id, class_inst)
            
