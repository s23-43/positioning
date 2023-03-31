import math
from typing import List, Tuple

def distance_between(a: Tuple[float, float], b: Tuple[float, float]) -> float:
	"""
	Calculates the distance between two coordinates in a 2D space using the Pythagorean theorem

	Args:
		a: A 2D coordinate
		b: A 2D coordinate

	Returns:
		The distance between the given 2D coordinates
	"""

	dxs = (a[0] - b[0])**2
	dys = (a[1] - b[1])**2
	return math.sqrt(dxs + dys)

def approximation_error(approx: float = 0, exact: float = 1) -> float:
	"""
	Calculates the approximation error between the given approximate and exact values. To get percent error, multiply the return value by 100

	Args:
		approx: The approximated value
		exact: The expected value

	Returns:
		The approximation error as a float. For example, if the error is 50%, then this function will return 0.5
	"""
	diff = (approx - exact)
	return abs(diff / exact)

def convert_string_list_to_floats(num_str: str) -> List[float]:
	"""
	Takes a string of numbers formatted with comma-separated numbers and returns a tuple-casted version. For example, if the string is "1,2.2,5,12", then the returned tuple will be (1.0, 2.2, 5.0, 12.0).

	Args:
		numStr: A comma-separated list of numbers

	Returns:
		A list with each number in the comma-separated list as its own entry in the list
	"""
	str_list = num_str.split(",")
	num_list = list()
	for s in str_list:
		num_list.append(float(s))
	return num_list