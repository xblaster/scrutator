'''
Created on 12 Nov 2009

@author: wax
'''
from scrutator.minidi.injector import *
from scrutator.core.manager import EventManager

from scrutator.core.event import *

import unittest

        
class TestCoreManager(unittest.TestCase):
    def testSingleton(self):
        self.assertEquals(id(CoreManager()), id(CoreManager()))

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