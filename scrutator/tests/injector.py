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
        
class TestCoreManager(unittest.TestCase):
    def testSingleton(self):
        self.assertEquals(id(CoreManager()), id(CoreManager()))

class TestXmlConfigUsage(unittest.TestCase):
    def testXMLConfig(self):
        context = Context()
        context.addConfig(XMLConfig("scrutator/tests/injector_test.xml"))
        self.assertEquals("bob",context.get_object("class1").name)
        self.assertEquals("robert",context.get_object("class2").name)


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