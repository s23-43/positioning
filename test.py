#!/usr/bin/env python3

import csv
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
		"""
		Initializes a collection of receivers. Lists of coodinates and gains must be equal in length.
		For every index, i, Receiver i is at position (x-coords[i], y-coords[i]) and has a gain of
		gains[i].

		Args:
			x_coords: List of receivers' x-coordinates
			y_corods: List of receivers' y-coordinates
			gains: List of receivers' gains

		Raises:
			Exception: If lists of x-coordinates, y-coordinates, and gains are not equal in length.
		"""
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
		"""
		Initializes a transmitter

		Args:
			gain: Transmitted antenna gain
			power: Transmitted signal power
			position: 2D position of transmitter
		"""
		self.set_position(position)
		self.gain = gain
		self.power = power
	def set_position(self, new_position: Tuple[float, float]) -> None:
		"""
		Sets the transmitter's position, setting both a 2-variable tuple and separate x- and y-coordinates

		Args:
			new_position: 2D position of transmitter

		Raises:
			Exception: If new position is not a 2-length tuple
		"""
		if len(new_position) != 2:
			raise Exception(f"Invalid transmitter position. Must be 2-dimensional tuple. Got: {new_position}")
		self.position = new_position
		self.x = new_position[0]
		self.y = new_position[1]

class ResultData:
	def __init__(self, pos_estm: Tuple[float, float] = (0, 0), time: float = 0):
		"""
		Initializes a class that stores resulting data from a single instance of a test

		Args:
			pos_estm: Estimated position of tracked object
			time: Time elapsed for estimation

		Raises:
			Exception: If position estimation is not a 2-length tuple
		"""
		if len(pos_estm) != 2:
			raise Exception(f"Invalid result position. Must be 2-dimensional tuple. Got: {pos_estm}")
		self.estimated_position = pos_estm
		self.x = pos_estm[0]
		self.y = pos_estm[1]
		self.elapsed_time = time

def calculate_real_received_powers(wavelength: float, tx: Transmitter, rx: Receivers, standard_deviation: float = 0) -> List[float]:
	"""
	Calculates received signal strength of each receiver. Has optional randomness parameter to simulate non-ideal conditions

	Args:
		wavelength: Wavelength of signal
		tx: Transmitter object
		rx: Receivers object
		standard_deviation (optional): Defines the standard deviation used for random-number generator to simulate non-ideal conditions

	Returns:
		A list of received signal strengths
	"""
	powers_rx = list()
	for x,y,g in zip(rx.x_coords, rx.y_coords, rx.gains):
		dist = util.distance_between(tx.position, (x,y))
		pwr = friis.standard_form(tx.power, tx.gain, g, wavelength, dist)
		if standard_deviation != 0:
			pwr += numpy.random.normal(0, standard_deviation)
		powers_rx.append(pwr)
	return powers_rx

def estimate_position_rss(rx: Receivers, powers: List[float]) -> Tuple[float, float]:
	"""
	Alternative experimental position estimation algorithm based on received signal strength. Not fully tested or vetted.

	Args:
		rx: Receivers object
		powers: List of received signal strengths

	Returns:
		Estimated location of tracked object as 2-length tuple
	"""
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

def test(wavelength: float, tx: Transmitter, rx: Receivers, standard_deviation: float = 0) -> ResultData:
	"""
	Runs single instance of simulated estimation. Calculates the expected distance between transmitter and each receiver to estimate position with optional randomness to simulate non-ideal conditions

	Args:
		wavelength: Wavelength of signal
		tx: Transmitter object
		rx: Receivers object
		standard_deviation (optional): Standard deviation of random number generator to simulate non-ideal conditions when calculating received signal strength

	Returns:
		A ResultData object with results from the simulation
	"""
	# Calculate received signal powers based on exact distances between the tracked object and observation points to prepare for simulating realistic path loss
	# If the randomness seed is set, then a random value will be generated and summed to each received path loss to simulate non-ideal conditions
	powers_rx = calculate_real_received_powers(wavelength, tx, rx, standard_deviation=standard_deviation)

	# Calculate distances between the tracked object and observation points based on the simulated path losses
	calculated_distances = list()
	for p,g in zip(powers_rx, rx.gains):
		calculated_distances.append( friis.distance_form(p, tx.power, g, tx.gain, wavelength) )

	start_time = time.time()
	roots = positioning.calculate_roots(rx.num, calculated_distances, rx.x_coords, rx.y_coords)
	estimated_position = positioning.estimate_position_by_roots(roots)
	end_time = time.time()

	return ResultData(estimated_position, end_time - start_time)

def plot(x_est: float, y_est: float, tx: Transmitter, rx: Receivers, round_amt=3) -> None:
	"""
	Plots the estimated location of the transmitter and the true locations of the receivers and transmitter on a 2D graph

	Args:
		x_est: Estimated x-position
		y_est: Estimated y-position
		tx: Transmitter object
		rx: Receivers object
		round_amt (optional): Number of decimal places to round values of coordinates that are displayed on the graph
	"""
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
		ax.annotate( f"OP{i}{op}", op )
	plt.show(block=True)

def main():
	tx = Transmitter(0, 0, (1,9))
	rx = Receivers( \
		[ 0.00, 0.00,  0.00, 5.00,  5.00, 10.00, 10.00, 10.00 ], \
		[ 0.00, 5.00, 10.00, 0.00, 10.00,  0.00,  5.00, 10.00 ], \
		[ 0.00, 0.00,  0.00, 0.00,  0.00,  0.00,  0.00,  0.00 ] \
	)
	try:
		rows = list()
		for x in range(1, 10):
			for y in range (1, 10):
				tx.set_position( (x,y) )
				result = test(0.1, tx, rx, standard_deviation=0.1)
				x_est = round(result.x, 3)
				y_est = round(result.y, 3)
				time = round(result.elapsed_time, 3)
				rows.append( [x, x_est, y, y_est, time] )
				print(f"{(x,y)} ~ {(x_est,y_est)}")
		with open ("results.csv", "w", newline='') as file:
			writer = csv.writer(file)
			writer.writerow( ["Real x", "Estimated x", "Real y", "Estimated y", "Elapsed time (s)"] )
			writer.writerows(rows)

	except Exception as e:
		print(e, file=sys.stderr)

if __name__ == "__main__":
	main()