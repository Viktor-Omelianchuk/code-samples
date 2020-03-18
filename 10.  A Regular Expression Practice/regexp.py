def calculate(data, findall):
	"""The function will find a number of simple arithmetic 
		expressions in the text and count them."""
    matches = findall(r"([abc](?=[+-]?=))([+-]?=)([abc])?([+-]?[0-9]+)?") 
    for v1, s, v2, n in matches:  

        if s == '=':
            data[v1] = data.get(v2, 0) + int(n or 0)
        elif s == '+=':
            data[v1] += data.get(v2, 0) + int(n or 0)
            print(data.get(v2, 0))
        elif s == "-=":
            data[v1] -= data.get(v2, 0) + int(n or 0)
            print(data.get(v2, 0))
    return data
