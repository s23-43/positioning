#!/usr/bin/env python3

import friis
import sys
import positioning
import numpy
import util

def friis_tests(pos_tx: tuple[float, float], wavelength: float, p_tx: float, g_tx: float, x_coords_rx: tuple[float, ...], y_coords_rx: tuple[float, ...], gains_rx: tuple[float, ...], seed: int | float | None = None) -> None:
	"""
	TODO: Add function description

	Args:
		pos_tx (tuple[float, float]): Position of transmitter ([m, m])
		wavelength (float): Wavelength of transmitted signal (m)
		p_tx (float): Signal power of transmitter (dBm)
		g_tx (float): Antenna gain of tracked object (dBi)
		x_coords_rx (tuple[float, ...]): Receivers' x-coordinate values in 2D plane ([m, ...])
		y_coords_rx (tuple[float, ...]): Receivers' y-coordinate values in 2D plane ([m, ...])
		gains_rx (tuple[float, ...]): List of receivers' antenna gains ([dBi, ...])
		seed (int | float | None): Optional parameter. Seed value for path loss randomness to simulate non-ideal conditions

	Returns
		TODO: Add return description

	Raises:
		TODO: Add exception descriptions
	"""
	if len(pos_tx) != 2:
		raise Exception(f"Object position must be a 2-float tuple. Invalid position: {pos_tx}")
	xc, yc = pos_tx[0], pos_tx[1]

	NUM = len(x_coords_rx)
	if NUM != len(y_coords_rx) or NUM != len(gains_rx):
		raise Exception(\
			"Observation points' tuples must match in length." + \
				f"\n\tOP x-coords ({len(x_coords_rx)}): {x_coords_rx}" + \
				f"\n\tOP y-coords ({len(y_coords_rx)}): {y_coords_rx}" + \
				f"\n\tOP gains ({len(gains_rx)}): {gains_rx}" \
		)

	if not (type(seed) is int or type(seed) is float or seed is None):
		raise Exception(f"Seed for path loss randomization has invalid type {type(seed)}: {seed}")

	# Get exact distances between tracked object and observation points
	distances = list()
	for x, y in zip(x_coords_rx, y_coords_rx):
		distances.append(util.pythagorean_theorem((x,y), (xc, yc)))

	# Get received signal powers
	powers_rx = list()
	for i in range(len(distances)):
		p_rx = friis.standard_form(p_tx, g_tx, gains_rx[i], wavelength, distances[i])
		if seed is not None:
			p_rx += numpy.random.normal(0, seed)
		powers_rx.append(p_rx)

	# Get estimated distances
	calculated_distances = list()
	for i in range(len(powers_rx)):
		calculated_distances.append(friis.distance_form(powers_rx[i], p_tx, gains_rx[i], g_tx, wavelength))

	# Estimate position based on estimated distances
	roots = positioning.calculate_roots(NUM, tuple(calculated_distances), x_coords_rx, y_coords_rx)
	print(f"Exact position:     {pos_tx}")
	print(f"Estimated position: {positioning.estimate_position(roots)}")

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
		friis_tests(pos_tx=(4,4), wavelength=0.1, p_tx=0, g_tx=0, x_coords_rx=x, y_coords_rx=y, gains_rx=g, seed=2)
		#pos_tests()
	except Exception as e:
		print(e, file=sys.stderr)

if __name__ == "__main__":
	main()