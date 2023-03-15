#!/usr/bin/env python3

import argparse
import sympy
import sys

def convert_string_list_to_floats(numStr:str) -> list:
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
		roots = list()
		funcs = list()
		x,y = sympy.symbols("x,y")
		for i in range(0, numOPs):
			funcs.append( sympy.Eq( \
				radii[i]**2, \
				x**2 - 2*xCoords[i]*x + xCoords[i]**2 + y**2 - 2*yCoords[i]*y + yCoords[i]**2 \
			))
		for i in range(0, numOPs):
			for j in range(i+1, numOPs):
				roots.append(sympy.solve([funcs[i], funcs[j]], (x,y)))
				print(roots[i])
		# TODO: Determine and print out the common root
	except Exception as e:
		print(e, file=sys.stderr)

if __name__ == "__main__":
	main()