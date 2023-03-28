#!/usr/bin/env python3

import friis
import numpy
import positioning
import sys
import time
import util
from typing import Tuple, Optional

def test(pos_tx: Tuple[float, float], wavelength: float, p_tx: float, g_tx: float, x_coords_rx: Tuple[float, ...], y_coords_rx: Tuple[float, ...], gains_rx: Tuple[float, ...], seed: Optional[float] = None) -> None:
	"""
	Runs a test that compares a tracked object's actual position with the position estimated by the positioning algorithm based on path losses. Randomess can optionally be added to path losses to simulate non-ideal conditions.

	Args:
		pos_tx: Position of transmitter ([m, m])
		wavelength: Wavelength of transmitted signal (m)
		p_tx: Signal power of transmitter (dBm)
		g_tx: Antenna gain of tracked object (dBi)
		x_coords_rx: Receivers' x-coordinate values in 2D plane ([m, ...])
		y_coords_rx: Receivers' y-coordinate values in 2D plane ([m, ...])
		gains_rx: List of receivers' antenna gains ([dBi, ...])
		seed (optional): Seed value for path loss randomness to simulate non-ideal conditions

	Raises:
		Exception: If tuple representing the tracked object's position does not have length of 2
		Exception: If tuples representing observation points' positions and gains do not have matching lengths
		Exception: If the seed for path loss randomization is not a numeric type or `None` type
	"""
	# Validate parameters
	if len(pos_tx) != 2:
		raise Exception(f"Object position must be a 2-float tuple. Invalid position: {pos_tx}")
	x_real, y_real = pos_tx[0], pos_tx[1]
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

	# Output test details
	print("Running test with the following setup:")
	print(f"- Signal of wavelength {wavelength}m transmitting from ({x_real}m, {y_real}m) with power of {p_tx}dBm and gain of {g_tx}dBi")
	for i,(x,y,g) in enumerate(zip(x_coords_rx, y_coords_rx, gains_rx)):
		print(f"- OP{i+1} receiving signal at {(x,y)} with gain of {g}dBi")

	# Calculate received signal powers based on exact distances between the tracked object and observation points to prepare for simulating realistic path loss
	# If the randomness seed is set, then a random value will be generated and summed to each received path loss to simulate non-ideal conditions
	powers_rx = list()
	for x,y,g in zip(x_coords_rx, y_coords_rx, gains_rx):
		dist = util.pythagorean_theorem((x,y), (x_real, y_real))
		p_rx = friis.standard_form(p_tx, g_tx, g, wavelength, dist)
		if seed is not None:
			p_rx += numpy.random.normal(0, seed)
		powers_rx.append(p_rx)

	# Calculate distances between the tracked object and observation points based on the simulated path losses
	calculated_distances = list()
	for p,g in zip(powers_rx, gains_rx):
		calculated_distances.append(friis.distance_form(p, p_tx, g, g_tx, wavelength))

	# Estimate the tracked object's position based on calculated distances. There should be as little overhead as possible between start_time and end_time so as not
	# to misrepresent/inflate the amount of time it takes to estimate position
	calculated_distances_tuple = tuple(calculated_distances)
	start_time = time.time()
	roots = positioning.calculate_roots(NUM, calculated_distances_tuple, x_coords_rx, y_coords_rx)
	estimated_pos = positioning.estimate_position(roots)
	end_time = time.time()
	x_estm, y_estm = estimated_pos

	# Calculate comparisons between actual and estimated values
	x_erro = util.approximation_error(exact=x_real, approx=x_estm) * 100
	y_erro = util.approximation_error(exact=y_real, approx=y_estm) * 100
	x_diff = abs(x_real - x_estm)
	y_diff = abs(y_real - y_estm)
	dist = util.pythagorean_theorem((x_real,y_real),(x_estm,y_estm))

	# Output results
	ROUND_AMT: int = 3
	print(f"Exact position:          ({round(x_real, ROUND_AMT)}m, {round(y_real, ROUND_AMT)}m)")
	print(f"Estimated position:      ({round(x_estm, ROUND_AMT)}m, {round(y_estm, ROUND_AMT)}m)")
	print(f"Estimation elapsed time: {round(end_time - start_time, 3)}sec")
	print(f"Percent difference:      ({round(x_erro, ROUND_AMT)}%, {round(y_erro, ROUND_AMT)}%)")
	print(f"Delta values:            ({round(x_diff, ROUND_AMT)}m, {round(y_diff, ROUND_AMT)}m)")
	print(f"Distance apart:          {round(dist, ROUND_AMT)}m")

def main():
	x = ( 0.00, 3.00, 10.00 )
	y = ( 0.00, 8.00,  5.00 )
	g = ( 0.00, 0.00,  0.00 )
	try:
		test(pos_tx=(4,4), wavelength=0.1, p_tx=0, g_tx=0, x_coords_rx=x, y_coords_rx=y, gains_rx=g, seed=4)
	except Exception as e:
		print(e, file=sys.stderr)

if __name__ == "__main__":
	main()