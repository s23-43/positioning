#!/usr/bin/env python3

import friis
import positioning

def friis_tests() -> None:
	pass

def pos_tests() -> None:
	radii   = [ 5.66, 4.12,  6.08, 4.24, 4.24 ]
	xCoords = [ 0.00, 3.00, 10.00, 7.00, 1.00 ]
	yCoords = [ 0.00, 8.00,  5.00, 7.00, 1.00 ]
	assert len(radii) == len(xCoords)
	assert len(radii) == len(yCoords)
	expectedPosition = (4,4)
	roots = positioning.calculate_roots(len(radii), radii, xCoords, yCoords)
	print(positioning.estimate_position(roots))
	pass

def main():
	pos_tests()

if __name__ == "__main__":
	main()