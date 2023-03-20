#!/usr/bin/env python3

import friis
import sys
import positioning

def friis_tests(obj_pos: tuple[float, float], wavelength: float, p_tx: float, g_tx: float, x_coords: tuple[float, ...], y_coords: tuple[float, ...], gains_rx: tuple[float, ...], seed: float | None) -> None:
	"""
	TODO: Add function description
	"""
	assert len(obj_pos) == 2
	NUM = len(x_coords)
	assert NUM == len(y_coords)
	assert NUM == len(gains_rx)

	xc, yc = obj_pos[0], obj_pos[1]
	distances = list()
	for x, y in zip(x_coords, y_coords):
		distances.append(positioning.pythag((x,y), (xc, yc)))
	powers_rx = list()
	for i in range(len(distances)):
		powers_rx.append(friis.standard_form(p_tx, g_tx, gains_rx[i], wavelength, distances[i], seed=seed))

	calculated_distances = list()
	for i in range(len(powers_rx)):
		calculated_distances.append(friis.distance_form(powers_rx[i], p_tx, gains_rx[i], g_tx, wavelength))
	print(calculated_distances)

	roots = positioning.calculate_roots(NUM, tuple(calculated_distances), x_coords, y_coords)
	print((xc, yc))
	print(positioning.estimate_position(roots))

def pos_tests() -> None:
	"""
	TODO: Add function description
	"""
	radii    = ( 5.66, 4.12,  6.08, 4.24, 4.24 )
	x_coords = ( 0.00, 3.00, 10.00, 7.00, 1.00 )
	y_coords = ( 0.00, 8.00,  5.00, 7.00, 1.00 )
	assert len(radii) == len(x_coords)
	assert len(radii) == len(y_coords)
	expectedPosition = (4,4)
	roots = positioning.calculate_roots(len(radii), radii, x_coords, y_coords)
	print(positioning.estimate_position(roots))

def main():
	x = ( 0.00, 3.00, 10.00 )
	y = ( 0.00, 8.00,  5.00 )
	g = ( 0.00, 0.00,  0.00 )
	try:
		friis_tests(obj_pos=(4,4), wavelength=0.1, p_tx=0, g_tx=0, x_coords=x, y_coords=y, gains_rx=g, seed=0)
		pos_tests()
	except Exception as e:
		print(e, file=sys.stderr)

if __name__ == "__main__":
	main()