class CallbackList(list):
	def execute(self, *args, **kwargs):
		for listener in self:
			listener(*args, **kwargs)