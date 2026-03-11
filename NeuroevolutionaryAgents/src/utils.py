def ClampFloat(variable : float, min_value : float, max_value : float):
	output = variable
	if variable < min_value:
		output = min_value
	elif variable > max_value:
		output = max_value
	return output