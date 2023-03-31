#!/usr/bin/env python3

import friis
import numpy
import positioning
import sys
import time
import util
from typing import List, Tuple
from matplotlib import pyplot as plt

class Receivers:
	def __init__(self, x_coords: List[float], y_coords: List[float], gains: List[float]):
		NUM = len(x_coords)
		if NUM != len(y_coords) or NUM != len(gains):
			raise Exception( \
				"Receivers' parameters must match in length:" + \
					f"\n\tx-coordinates ({len(x_coords)}): {x_coords}" + \
					f"\n\ty-coordinates ({len(y_coords)}): {y_coords}" + \
					f"\n\tgain values ({len(gains)}): {gains}" \
			)
		self.num = NUM
		self.x_coords = x_coords
		self.y_coords = y_coords
		self.gains = gains

class Transmitter:
	def __init__(self, gain: float, power: float, position: Tuple[float, float]):
		if len(position) != 2:
			raise Exception(f"Invalid transmitter position. Must be 2-dimensional: {position}")
		self.gain = gain
		self.power = power
		self.position = position
		self.x = position[0]
		self.y = position[1]

def calculate_real_received_powers(wavelength: float, tx: Transmitter, rx: Receivers, standard_deviation: float = 0) -> List[float]:
	powers_rx = list()
	for x,y,g in zip(rx.x_coords, rx.y_coords, rx.gains):
		dist = util.distance_between(tx.position, (x,y))
		pwr = friis.standard_form(tx.power, tx.gain, g, wavelength, dist)
		if standard_deviation != 0:
			pwr += numpy.random.normal(0, standard_deviation)
		powers_rx.append(pwr)
	return powers_rx

def estimate_position_rss(rx: Receivers, powers: List[float]) -> Tuple[float, float]:
	x_est = 0
	y_est = 0
#	power_avg_db = numpy.average(powers_rx)
#	power_avg_linear = 10**(power_avg_db/10)
	power_avg_linear = 0
	for p in powers:
		power_avg_linear += 10**(p/10)
	power_avg_linear = power_avg_linear / len(powers)
	# print(f"Average received power: {power_avg_linear}")
	for i in range(0, len(rx.x_coords)):
		# print(f"{x_coords[i]}, {y_coords[i]}, {powers_rx[i]}")
		x_est += rx.x_coords[i] * 10**(powers[i]/10)
		y_est += rx.y_coords[i] * 10**(powers[i]/10)
	x_est = ( x_est / len(rx.x_coords) ) / power_avg_linear
	y_est = ( y_est / len(rx.y_coords) ) / power_avg_linear
	return (x_est, y_est)

def test(wavelength: float, tx: Transmitter, rx: Receivers, standard_deviation: float = 0) -> None:
	# Output test details
	print("Running test with the following setup:")
	print(f"- Signal of wavelength {wavelength}m transmitting from {tx.position} with power of {tx.power}dBm and gain of {tx.gain}dBi")
	for i,(x,y,g) in enumerate(zip(rx.x_coords, rx.y_coords, rx.gains)):
		print(f"- OP{i+1} receiving signal at {(x,y)} with gain of {g}dBi")

	# Calculate received signal powers based on exact distances between the tracked object and observation points to prepare for simulating realistic path loss
	# If the randomness seed is set, then a random value will be generated and summed to each received path loss to simulate non-ideal conditions
	powers_rx = calculate_real_received_powers(wavelength, tx, rx, standard_deviation=standard_deviation)

	print(tx.position)
	estimate_position_rss(rx, powers_rx)

	# Calculate distances between the tracked object and observation points based on the simulated path losses
	calculated_distances = list()
	for p,g in zip(powers_rx, rx.gains):
		calculated_distances.append( friis.distance_form(p, tx.power, g, tx.gain, wavelength) )

	roots = positioning.calculate_roots(rx.num, calculated_distances, rx.x_coords, rx.y_coords)
	print(positioning.estimate_position_by_roots(roots))

def plot(x_est: float, y_est: float, tx: Transmitter, rx: Receivers, round_amt=3) -> None:
	# Visualize positions
	real = round(tx.x, round_amt), round(tx.y, round_amt)
	estm = round(x_est, round_amt), round(y_est, round_amt)
	_, ax = plt.subplots()
	plt.plot(tx.x, tx.y, '*')
	ax.annotate( f"actual {real}", real )
	plt.plot(x_est, y_est, 'o')
	ax.annotate( f"estimate {estm}", estm )
	for i,(x,y) in enumerate( zip(rx.x_coords, rx.y_coords) ):
		op = round(x, round_amt), round(y, round_amt)
		plt.plot(x, y, '.')
		ax.annotate( f"OP{i+1}{op}", op )
	plt.show(block=True)

def main():
#	x = ( 0.00, 3.00, 10.00 )
#	y = ( 0.00, 8.00,  5.00 )
#	g = ( 0.00, 0.00,  0.00 )
	tx = Transmitter(0, 0, (5,5))
	rx = Receivers( \
		[ 0.00, 0.00,  0.00, 5.00,  5.00, 10.00, 10.00, 10.00 ], \
		[ 0.00, 5.00, 10.00, 0.00, 10.00,  0.00,  5.00, 10.00 ], \
		[ 0.00, 0.00,  0.00, 0.00,  0.00,  0.00,  0.00,  0.00 ] \
	)
	try:
		# for sd in range(0, 11):
		# 	print(f"sd {sd}:")
		# 	for _ in range(1, 10):
		# 		test(wavelength=0.1, tx=tx, rx=rx, standard_deviation=sd)
		# 		time.sleep(0.5)
		test(wavelength=0.1, tx=tx, rx=rx)
	except Exception as e:
		print(e, file=sys.stderr)

if __name__ == "__main__":
	main()