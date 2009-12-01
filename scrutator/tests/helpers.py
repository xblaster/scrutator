#!/usr/bin/env python
# encoding: utf-8
import unittest

from scrutator.helpers import url
from remote.services.helpers import *

class TestUriHelper(unittest.TestCase):
		
	def testUrlDetection(self):
		to_catch = "salut, j'ai trouvé une super url => http://www.lo2k.net"
		self.assertEqual("http://www.lo2k.net", url.detect_link(to_catch))
		
		to_catch = "plop bob. Ecoute www.lo2k.net c'est trop bien"
		self.assertEqual("www.lo2k.net", url.detect_link(to_catch))
		
		to_catch = "http://bashfr.org nous a quoté"
		self.assertEqual("http://bashfr.org", url.detect_link(to_catch))
		
		to_catch = "bashfr.org nous a quoté"
		self.assertEqual(None, url.detect_link(to_catch))

		
	def testCommentDetection(self):
		to_catch = "salut, j'ai trouvé une super url    => http://www.lo2k.net"
		self.assertEqual("salut, j'ai trouvé une super url", url.get_comment(to_catch))
		
		to_catch = "salut, j'ai trouvé une super url <= http://www.lo2k.net"
		self.assertEqual("salut, j'ai trouvé une super url", url.get_comment(to_catch))
		
		to_catch = "http://bashfr.org"
		self.assertEqual(None, url.get_comment(to_catch))
		
	def testComputerName(self):
		name = "maury/5161-13513-153153-15313"
		self.assertEqual("maury", getComputername(name))
		
		name = "oil-ocean/5161-13513-153153-15313"
		self.assertEqual("oil-ocean", getComputername(name))
		
