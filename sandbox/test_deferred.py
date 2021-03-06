from twisted.internet import defer
from twisted.internet import threads, reactor
import random
from time import sleep

def printResult(result):
	res = 0
	for (success, value) in result:
		if success:
			print 'Success:', value
			res = res + value
		else:
			print 'Failure:', value.getErrorMessage()
	print "total: " + str(res)
	reactor.stop()

def calc(number):
	sleep(random.randint(0, 10))
	print "calc number " + str(number)	
	return number * number

def massCalc():
	defer_list = list()
	for i in range(20):
		d = threads.deferToThread(calc, i)
		defer_list.append(d)
	
	print "create defer list"	
	dl = defer.DeferredList(defer_list)
	dl.addCallback(printResult)

reactor.callLater(2, massCalc)
reactor.run()
