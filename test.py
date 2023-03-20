#!/usr/bin/env python3

import friis
import sys
import positioning
import numpy
import util

def test(pos_tx: tuple[float, float], wavelength: float, p_tx: float, g_tx: float, x_coords_rx: tuple[float, ...], y_coords_rx: tuple[float, ...], gains_rx: tuple[float, ...], seed: int | float | None = None) -> None:
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

	# Calculate received signal powers based on exact distances between the tracked object and observation points to prepare for simulating realistic path loss
	# If the randomness seed is set, then a random value will be generated and summed to each received path loss to simulate non-ideal conditions
	powers_rx = list()
	for x,y,g in zip(x_coords_rx, y_coords_rx, gains_rx):
		dist = util.pythagorean_theorem((x,y), (xc, yc))
		p_rx = friis.standard_form(p_tx, g_tx, g, wavelength, dist)
		if seed is not None:
			p_rx += numpy.random.normal(0, seed)
		powers_rx.append(p_rx)

	# Calculate distances between the tracked object and observation points based on the simulated path losses
	calculated_distances = list()
	for i in range(len(powers_rx)):
		calculated_distances.append(friis.distance_form(powers_rx[i], p_tx, gains_rx[i], g_tx, wavelength))

	# Estimate the tracked object's position based on calculated distances
	roots = positioning.calculate_roots(NUM, tuple(calculated_distances), x_coords_rx, y_coords_rx)
	print(f"Exact position:     {pos_tx}")
	print(f"Estimated position: {positioning.estimate_position(roots)}")

def main():
	x = ( 0.00, 3.00, 10.00 )
	y = ( 0.00, 8.00,  5.00 )
	g = ( 0.00, 0.00,  0.00 )
	try:
		test(pos_tx=(4,4), wavelength=0.1, p_tx=0, g_tx=0, x_coords_rx=x, y_coords_rx=y, gains_rx=g, seed=2)
	except Exception as e:
		print(e, file=sys.stderr)

if __name__ == "__main__":
	main()