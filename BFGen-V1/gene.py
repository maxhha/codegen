import brainfuck
import random

LOOP_LIMIT = 1024

class Gene:
	def __init__(self, code="", mem_size = 16):
		self.code = code
		self.mem_size = mem_size
	
	def run(self, output_size=None, data=[]):
		global LOOP_LIMIT
		if output_size == None:
			output_size = self.mem_size
		result = brainfuck.run(self.code, self.mem_size, LOOP_LIMIT, data)
		data = result["data"]
		if len(data) < output_size:
			return data + [0]*(output_size - len(data))
		else:
			return data[-output_size:]
	
	def copy_from(self, gene):
		self.code = gene.code
		self.mem_size = gene.mem_size
		return self
	
	def clone(self):
		return Gene().copy_from(self)
	
	def mutate(self, number_mutations=0):
		code = list(self.code)
		for _ in range(number_mutations):
			t = random.randrange(5 + int(len(code) > 0))
			c = random.random() > 0.5#insert value
			if t == 5:
				x = random.randrange(len(code))
				l = random.randrange(len(code)-x)+1
				for i in range(l-1, -1, -1):
					del code[x+i]
			elif t == 4:
				if len(code) < 2:
					code = ["[","]"]
				else:
					x1 = x2 = 0
					while x1 == x2:
						x1 = random.randrange(len(code) + int(c))
						x2 = random.randrange(len(code) + int(c))
					
					if x1 > x2:
						x1, x2 = x2, x1
				
					if c:
						code.insert(x2, "]")
						code.insert(x1, "[")
					else:
						code[x1] = "["
						code[x2] = "["
			else:
				if len(code) < 1:
					c = True
				x = random.randrange(len(code) + int(c))
				if c:
					code.insert(x, "+-><"[t])
				else:
					code[x] = "+-><"[t]
		self.code = "".join(code)
		self.fix_code()
		return self
	
	def fix_code(self):
		r = 0
		l = 0
		for c in self.code:
			if c == "[":
				r += 1
			elif c == "]":
				if r == 0:
					l += 1
				else:
					r -= 1
		self.code = "[" * l + self.code + "]" * r