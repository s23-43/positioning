def pythagorean_theorem(a: tuple[float, float], b: tuple[float, float]) -> float:
	"""
	Calculates the distance between two coordinates in a 2D space using the Pythagorean theorem

	Args:
		a (tuple[float, float]): A 2D coordinate
		b (tuple[float, float]): A 2D coordinate

	Returns:
		The distance between the given 2D coordinates
	"""

	dxs = (a[0] - b[0])**2
	dys = (a[1] - b[1])**2
	return (dxs + dys)**0.5

def convert_string_list_to_floats(num_str: str) -> tuple[float, ...]:
	"""
	Takes a string of numbers formatted with comma-separated numbers and returns a tuple-casted version. For example, if the string is "1,2.2,5,12", then the returned tuple will be (1.0, 2.2, 5.0, 12.0).

	Args:
		numStr (str): A comma-separated list of numbers

	Returns:
		A list with each number in the comma-separated list as its own entry in the list
	"""
	str_list = num_str.split(",")
	num_list = list()
	for s in str_list:
		num_list.append(float(s))
	return tuple(num_list)