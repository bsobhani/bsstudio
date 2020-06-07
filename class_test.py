class A:
	def a(self):
		return 7
	def a(self, val):
		return 8

a = A()
print(a.a())
print(a.a(2))
