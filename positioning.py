#!/usr/bin/env python3

import argparse
import sympy
import sys
import util

def calculate_roots(num: int, radii: tuple, x_coords: tuple, y_coords: tuple) -> tuple:
	"""
	TODO: Add function description
	"""
	funcs = list()
	x,y = sympy.symbols("x,y")
	for i in range(0, num):
		funcs.append( sympy.Eq( \
			radii[i]**2, \
			x**2 - 2*x_coords[i]*x + x_coords[i]**2 + y**2 - 2*y_coords[i]*y + y_coords[i]**2 \
		))

	roots = list()
	for i in range(0, num):
		for j in range(i+1, num):
			roots.append(sympy.solve([funcs[i], funcs[j]], (x,y)))
	return tuple(roots)

def estimate_position(roots: tuple, show_complex: bool = False) -> tuple[float, float]:
	"""
	Estimates position based on the given list of roots of the intersecting circles. TODO: Once it's complete, explain how the estimate works

	Args:
		roots (list): A list of roots of the intersecting circles
		show_complex (bool): Optional flag. Roots are sometimes complex and are ignored by the estimation, so this flag determines whether or not to print notifications whenever a complex root is found

	Returns:
		The estimated position as a 2D coordinate represented by a tuple of 2 floats
	"""
	sum_x, sum_y, total = 0, 0, 0
	for root in roots:
		for coord in root:
			assert len(coord) == 2
			try:
				sum_x += float(coord[0])
				sum_y += float(coord[1])
				total += 1
			except Exception as e:
				if str(e) == "Cannot convert complex to float":
					if show_complex:
						print(f"Found complex root: {coord}. Safe to disregard.", file=sys.stdout)
				else:
					raise e
	# TODO: Estimate the position by finding roots that are closest together in value. Averaging is a temporary solution and is very inaccurate
	avg_x = sum_x / total
	avg_y = sum_y / total
	return (avg_x, avg_y)

def main():
	# Parse arguments
	parser = argparse.ArgumentParser()
	parser.add_argument("-r", type=str, required=True, help="List of radii calcualted from Friis transmission equation")
	parser.add_argument("-x", type=str, required=True, help="List of observation points' x-coordinates")
	parser.add_argument("-y", type=str, required=True, help="List of observation points' y-coordinates")
	args = parser.parse_args()

	try:
		# Convert given list of radii (string) to tuple of floats and verify their validity
		radii = util.convert_string_list_to_floats(args.r)
		for r in radii:
			if r < 0:
				raise Exception(f"Found invalid radius: {r}")

		# Convert given list of OP coordinates (strings) to tuples of floats
		xCoords = util.convert_string_list_to_floats(args.x)
		yCoords = util.convert_string_list_to_floats(args.y)

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