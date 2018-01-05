class Fib:
	'''菲波列契数列生成器，允许迭代，位置索引和切片（允许步进，但是不允许反向索引，因为数列是无限的）
	   示例:
	   Fib()[3];
	   
	   Fib()[[3]:10[:2]];
	   
	   for i in Fib():
	       if i > 100:
	           break
	       print(i)
	'''
	def __init__(self):
		self.a, self.b = 0, 1
	def __iter__(self):
		return self
	def __next__(self):
		self.a, self.b = self.b, self.a+self.b
		return self.a
	def __getitem__(self, n, m=1):
		if isinstance(n, int):
			for i in range(n):
				self.a, self.b = self.b, self.a+self.b
			return self.a
		if isinstance(n, slice):
			start = n.start
			stop = n.stop
			step = n.step
			if start == None:
				start = 0
			if step == None:
				step = 1
			L = list()
			flag = 1
			for i in range(stop):
				self.a, self.b = self.b, self.a+self.b
				if i == start:
					L.append(i-1)
				if i > start:
					flag += 1
					if step == flag:
						L.append(self.a)
						flag = 0
			return L

