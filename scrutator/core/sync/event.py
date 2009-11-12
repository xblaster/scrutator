# -*- coding: utf-8 -*-
import scrutator.core.event 

class FileRequestError(scrutator.core.event.SimpleEvent):
	pass

class FileRequest(scrutator.core.event.SimpleEvent):
	pass

class FileContent(scrutator.core.event.SimpleEvent):
	pass
