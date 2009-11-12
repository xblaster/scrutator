#!/usr/bin/env python
# encoding: utf-8
"""
spring.py

Created by Jérôme Wax on 2009-11-09.
Copyright (c) 2009 __MyCompanyName__. All rights reserved.
"""

import sys
import os

from springpython.config import *
from springpython.context import *


class User:
	def __init__(self, name="Elodie"):
		print "hello"
		print name
		pass

class TestApplicationContext(PythonConfig):
    def __init__(self):
        super(TestApplicationContext, self).__init__()

    @Object(scope.SINGLETON)
	
    def UserName(self):
		return "bob"
	
    def User(self):
        return User(self.app_context.get_object("UserName"))

def main():
	context = ApplicationContext(TestApplicationContext())
	user = context.get_object("User")


if __name__ == '__main__':
	main()




