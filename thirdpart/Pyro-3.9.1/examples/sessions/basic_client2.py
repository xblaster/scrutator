#!/usr/bin/env python
import Pyro.core
import threading, time, copy

NUMTHREADS = 5

testProxy = Pyro.core.getProxyForURI("PYRONAME://:test.threadstorage")

print "Will make copy of the proxy for every thread."
print "Observe in the server console that the TLS counter is now unique per proxy."

def processing(index, proxy):
	print 'Processing started', index
	while threading.currentThread().running:
		t1 = time.time()
		print index, "CALLING...."
		proxy.process("thread_" + str(index))
		time.sleep(NUMTHREADS + 1)
	print "exiting thread", index


# start a set of threads which perform requests

threads = []
for i in range(NUMTHREADS):
	proxy = copy.copy(testProxy)
	thread = threading.Thread(target=processing, args=(i, proxy))
	threads.append(thread)
	thread.running = True
	time.sleep(0.5)
	thread.start()

void = raw_input('\nPress enter to stop...\n\n')
print "Stopping threads."
for p in threads:
	p.running = False
for p in threads:
	p.join()
	print 'stopped', p.getName()

print 'Graceful exit.'
