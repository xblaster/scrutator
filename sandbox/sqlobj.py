from sqlobject import *

#sqlhub.processConnection = connectionForURI('sqlite:/:memory:')
sqlhub.processConnection = connectionForURI('mysql://root:Li23nux78@localhost/test')
class Person(SQLObject):
	fname = StringCol()
	mi = StringCol(length=1, default=None)
	lname = StringCol()

	

#class Link(SQLObject):
#    class sqlmeta:
#        fromDatabase = True

#Person.createTable()

#p = Person(fname="John", lname="Doe")
#p
#p.fname

#p.mi = 'Q'
p2 = Person.get(5)
print p2
print p is p2
