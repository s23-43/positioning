#!/usr/bin/env python3

import friis
import sys
import positioning
import util

def friis_tests(obj_pos: tuple[float, float], wavelength: float, obj_power: float, obj_gain: float, op_x_coords: tuple[float, ...], op_y_coords: tuple[float, ...], op_gains: tuple[float, ...], seed: int | float | None = None) -> None:
	"""
	TODO: Add function description

	Args:
		obj_pos (tuple[float, float]): Object position in 2D coordinate system (m, m)
		wavelength (float): Wavelength of signal (m)
		obj_power (float): Signal power of SDR on tracked object (dBm)
		obj_gain (float): Antenna gain of tracked object (dBi)
		op_x_coords (tuple[float, ...]): x-coordinate values representing positions of observation points ([m, ...])
		op_y_coords (tuple[float, ...]): y-coordinate values representing positions of observation points ([m, ...])
		op_gains (tuple[float, ...]): List of antenna gains of observation points ([dBi, ...])
		seed (int | float | None): Optional parameter. Seed value for path loss randomness to simulate non-ideal conditions

	Returns
		TODO: Add return description
	"""
	if len(obj_pos) != 2:
		raise Exception(f"Object position must be a 2-float tuple. Invalid position: {obj_pos}")
	xc, yc = obj_pos[0], obj_pos[1]

	NUM = len(op_x_coords)
	if NUM != len(op_y_coords) or NUM != len(op_gains):
		raise Exception(\
			"Observation points' tuples must match in length.\n" + \
				f"\tOP x-coords ({len(op_x_coords)}): {op_x_coords}\n" + \
				f"\tOP y-coords ({len(op_y_coords)}): {op_y_coords}\n" + \
				f"\tOP gains ({len(op_gains)}): {op_gains}" \
		)

	if not (type(seed) is int or type(seed) is float or seed is None):
		raise Exception(f"Seed for path loss randomization has invalid type {type(seed)}: {seed}")

	# Get exact distances between tracked object and observation points
	distances = list()
	for x, y in zip(op_x_coords, op_y_coords):
		distances.append(util.pythagorean_theorem((x,y), (xc, yc)))
	powers_rx = list()
	for i in range(len(distances)):
		powers_rx.append(friis.standard_form(obj_power, obj_gain, op_gains[i], wavelength, distances[i]))

	calculated_distances = list()
	for i in range(len(powers_rx)):
		calculated_distances.append(friis.distance_form(powers_rx[i], obj_power, op_gains[i], obj_gain, wavelength))
	print(calculated_distances)

	roots = positioning.calculate_roots(NUM, tuple(calculated_distances), op_x_coords, op_y_coords)
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
		friis_tests(obj_pos=(4,4), wavelength=0.1, obj_power=0, obj_gain=0, op_x_coords=x, op_y_coords=y, op_gains=g, seed=2)
		#pos_tests()
	except Exception as e:
		print(e, file=sys.stderr)

if __name__ == "__main__":
	main()