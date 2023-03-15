#!/usr/bin/env python3

import argparse
import sympy
import sys

def convert_string_list_to_floats(numStr: str) -> list:
	"""
	Takes a string of numbers formatted with comma-separated numbers and returns a tuple-casted version. For example, if the string is "1,2.2,5,12", then the returned tuple will be (1.0, 2.2, 5.0, 12.0).

	Args:
		numStr (str): A comma-separated list of numbers

	Returns:
		A list with each number in the comma-separated list as its own entry in the list
	"""
	strList = numStr.split(",")
	numList = []
	for s in strList:
		numList.append(float(s))
	return numList

def calculate_roots(num: int, radii: list, xCoords: list, yCoords: list) -> list:
	"""
	TODO: Add function description
	"""
	funcs = list()
	x,y = sympy.symbols("x,y")
	for i in range(0, num):
		funcs.append( sympy.Eq( \
			radii[i]**2, \
			x**2 - 2*xCoords[i]*x + xCoords[i]**2 + y**2 - 2*yCoords[i]*y + yCoords[i]**2 \
		))

	roots = list()
	for i in range(0, num):
		for j in range(i+1, num):
			roots.append(sympy.solve([funcs[i], funcs[j]], (x,y)))
	return roots

def estimate_position(roots: list) -> tuple[float, float]:
	"""
	TODO: Add function description
	"""
	coords = set()
	for root in roots:
		for coord in root:
			assert len(coord) == 2
			try:
				x = float(coord[0])
				y = float(coord[1])
				coords.add( (x,y) )
			except Exception as e:
				if str(e) == "Cannot convert complex to float":
					print(f"Found complex root: {coord}. Safe to disregard.", file=sys.stdout)
				else:
					raise e
	# TODO: Estimate the position by iterating through the remaining coords
	return (0,0)

def pythag(a: tuple, b: tuple) -> float:
	"""
	Calculates distance between two 2D coordinates using the Pythagorean theorem

	Args:
		a (tuple): A 2D coordinate
		b (tuple): A 2D coordinate

	Returns:
		The distance between the given coordinates
	"""
	assert len(a) == 2
	assert len(b) == 2
	x = ( a[0] - b[0] )**2
	y = ( a[1] - b[1] )**2
	return (x+y)**0.5

def main():
	# Parse arguments
	parser = argparse.ArgumentParser()
	parser.add_argument("-r", type=str, required=True, help="List of radii calcualted from Friis transmission equation")
	parser.add_argument("-x", type=str, required=True, help="List of observation points' x-coordinates")
	parser.add_argument("-y", type=str, required=True, help="List of observation points' y-coordinates")
	args = parser.parse_args()

	try:
		# Convert given list of radii (string) to tuple of floats and verify their validity
		radii = convert_string_list_to_floats(args.r)
		for r in radii:
			if r < 0:
				raise Exception(f"Found invalid radius: {r}")

		# Convert given list of OP coordinates (strings) to tuples of floats
		xCoords = convert_string_list_to_floats(args.x)
		yCoords = convert_string_list_to_floats(args.y)

		# Verify that tuples of radii, x-coords, and y-coords are same length
		if len(radii) != len(xCoords) or len(radii) != len(yCoords):
			raise Exception(f"Mismatched sizes of lists:\n  {len(radii)} radii\n  {len(xCoords)} x-coords\n  {len(yCoords)} y-coords")
		numOPs: int = len(radii)

		# Estimate and print position
		roots = calculate_roots(numOPs, radii, xCoords, yCoords)
		print(estimate_position(roots))
	except Exception as e:
		print(e, file=sys.stderr)

if __name__ == "__main__":
	main()