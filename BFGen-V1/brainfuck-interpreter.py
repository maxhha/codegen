def interpretate(code, mem_size, cycle_limit, head_mem=[]):
	py_code = "ptr = 0\n"
	tabs = 0
	data = head_mem + [0] * (mem_size - len(head_mem))
	
	for c in code:
		if c in "+-":
			py_code += "\t"*tabs + "data[ptr] = 1\n"
		elif c == ">":
			py_code += "\t"*tabs + "ptr = (ptr + 1) % mem_size\n"
		elif c == "<":
			py_code += "\t"*tabs + "ptr = (ptr + mem_size - 1) % mem_size\n"
		elif c == "[":
			e = "e"+str(tabs)
			pycode += "\t"*tabs +e+"=0\n"
			pycode += "\t"*tabs + "while(data[ptr] and "+e+"<cycle_limit):\n"
			tabs += 1
		elif c == "]":
			e = "e"+str(tabs-1)
			pycode += "\t"*tabs + e+"+=1\n"
			tabs -= 1
			pycode += "\t"*tabs + "if "+e+" >= cycle_limit:\n" + "\t"*tabs + "\treturn 1\n"
			
	pycode += "return 0"
	error = exec(py_code, {"data":data, "mem_size":mem_size, "cycle_limit":cycle_limit})
	return {"error":error, "data":data}