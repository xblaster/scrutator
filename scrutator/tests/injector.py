'''
Created on 12 Nov 2009

@author: wax
'''
from scrutator.minidi.injector import *
from scrutator.core.manager import EventManager

from scrutator.core.event import *

import unittest



class MockupClass:
    def __init__(self, name="bob"):
        self.name = name

class User:
    #class for unit test purpose
    def __init__(self, firstname, lastname):
        self.firstName = firstname
        self.lastName = lastname
        

class MockupPythonConfig(PythonConfig):
    def User(self):
        return User("bob","morane")
        
    def Mixed(self):
        res = User("bob","morane")
        res.class1 = self.getContext().get_object("class1")
        return res
        
class TestCoreManager(unittest.TestCase):
    def testSingleton(self):
        self.assertEquals(id(CoreManager()), id(CoreManager()))

class TestConfigUsage(unittest.TestCase):
    def testXMLConfig(self):
        context = Context()
        context.addConfig(XMLConfig("scrutator/tests/injector_test.xml"))
        self.assertEquals("bob",context.get_object("class1").name)
        self.assertEquals("robert",context.get_object("class2").name)

    def testPythonConfig(self):
        context = Context()
        context.addConfig(MockupPythonConfig())
        self.assertEquals("bob",context.get_object("User").firstName)
        user = context.get_object("User")
        user2 = context.get_object("User")
        self.assertEquals(user, user2)
        
    def testMixedConfig(self):
        context = Context(XMLConfig("scrutator/tests/injector_test.xml"),MockupPythonConfig())
        self.assertEquals("bob",context.get_object("Mixed").class1.name)


class TestXmlContext(unittest.TestCase):
    def testLoadBasicXML(self):
        context = Context()
        XMLBeanFactory("scrutator/tests/injector_test.xml", context)
        
        self.assertEquals("bob",context.get_object("class1").name)
        self.assertEquals("robert",context.get_object("class2").name)
        
class TestXml(unittest.TestCase):
    def testLoad(self):
        xeml = XmlEventManagerLoader()
        em = EventManager()
        xeml.load('resource/sample.xml', em)
        
        em.push(BanEvent())
        
        try: 
            em.push(KickEvent())
        except Exception:
            pass
        else:
            self.fail("expected an exception from ExceptionListener")