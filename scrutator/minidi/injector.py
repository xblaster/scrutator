'''
Created on 12 Nov 2009

@author: wax
'''

from scrutator.minidi.tool import smart_load

class CoreManager:
    """ A python singleton """

    class __CoreManagerimpl:
        """ Implementation of the singleton interface """
        from scrutator.core.manager import EventManager 
        beans_list = dict()
        
        eventManager = EventManager()
        
        def __init__(self):
            pass
        
        def push(self, eventObj):
            return self.eventManager.push(eventObj)
            
        def getEventManager(self):
            return self.eventManager
            
        def getBean(self, beanName):
            if self.beans_list.has_key(beanName):
                return self.beans_list[beanName]
            raise Exception('bean ' + str(beanName) + ' does not exist')
    
        def setBean(self, beanName, beanObj):
            self.beans_list[beanName] = beanObj


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
    
    def getListener(self, xmlNode):
        if xmlNode.hasAttribute('listener'):
            listenerName = xmlNode.getAttribute('listener')
            listenerClass = smart_load(listenerName)()
            return listenerClass
            
        if xmlNode.hasAttribute('bean'):
            beanName = xmlNode.getAttribute('bean')
            listenerClass = CoreManager().getBean(beanName)
            return listenerClass
        raise Exception('listener or bean')

    
    def load(self, filename, eventManager):
        from xml.dom.minidom import parse
        from sys import path
        resource_name = path[0] + '/' + filename
        
        doc = parse(resource_name)
        
        for trigger in doc.getElementsByTagName('trigger'):
            eventName = trigger.getAttribute('event')

            
            #if it's not "all" events
            if not eventName == 'all':
                eventName = smart_load(eventName)().getType()
            
            
            eventManager.bind(eventName, self.getListener(trigger))
