#!/usr/bin/env python3

import friis
import positioning

def friis_tests() -> None:
	xc,yc = (4, 4)
	wavelength = 0.1
	xCoords = [ 0.00, 3.00, 10.00 ]
	yCoords = [ 0.00, 8.00,  5.00 ]
	power_tx = 0
	gain_tx = 0
	gain_rx = [0, 0, 0]
	distances = list()
	for x, y in zip(xCoords, yCoords):
		distances.append(positioning.pythag((x,y), (xc, yc)))
	powers_rx = list()
	for i in range(len(distances)):
		powers_rx.append(friis.calculate_power_rx_log_normal(power_tx, gain_tx, gain_rx[i], wavelength, distances[i], 5))

	calculated_distances = list()
	for i in range(len(powers_rx)):
		calculated_distances.append(friis.calculate_distance(powers_rx[i], power_tx, gain_rx[i], gain_tx, wavelength))
	print(calculated_distances)

	roots = positioning.calculate_roots(len(calculated_distances), calculated_distances, xCoords, yCoords)
	print((xc, yc))
	print(positioning.estimate_position(roots))

def pos_tests() -> None:
	radii   = [ 5.66, 4.12,  6.08, 4.24, 4.24 ]
	xCoords = [ 0.00, 3.00, 10.00, 7.00, 1.00 ]
	yCoords = [ 0.00, 8.00,  5.00, 7.00, 1.00 ]
	assert len(radii) == len(xCoords)
	assert len(radii) == len(yCoords)
	expectedPosition = (4,4)
	roots = positioning.calculate_roots(len(radii), radii, xCoords, yCoords)
	print(positioning.estimate_position(roots))

def main():
	friis_tests()

if __name__ == "__main__":
	main()