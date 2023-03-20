#!/usr/bin/env python3

import argparse
import numpy
import math
import sys

def standard_form(power_tx: float, gain_tx: float, gain_rx: float, wavelength: float, distance: float) -> float:
	"""
	Calculates received power using the standard form of the Friis transmission equation
	Friis transmission equation (standard form):
		Pr[dBm] = Pt[dBm] + Gt[dBi] + Gr[dBi] + 20*log10(λ/(4πd))

	Args:
		power_tx (float): Signal power of transmitter (dBm)
		gain_tx (float): Antenna gain of transmitter (dBi)
		gain_rx (float): Antenna gain of receiver (dBi)
		wavelength (float): Wavelength of signal (m)
		distance (float): Distance between transmitter and receiver (m)

	Returns:
		Signal power of receiver (dBm)

	Raises:
		Exception when standard_deviation is not a float
	"""

	return power_tx + gain_tx + gain_rx + 20*math.log10(wavelength / (4 * math.pi * distance))

def distance_form(power_rx: float, power_tx: float, gain_rx: float, gain_tx: float, wavelength: float) -> float:
	"""
	Calculates the distance between a receiver and a transmitter using the decibel form of the Friis transmission equation
	Friis transmission equation (distance-isolated form):
		d = λ / (4π * 10^( ((Pr[dBm] - Pt[dBm] - Gt[dBi] - Gr[dBi]) / 20) )

	Args:
		power_rx (float): The signal power of the receiver (dBm)
		power_tx (float): The signal power of the transmitter (dBm)
		gain_rx (float): The antenna gain of the receiver (dBi)
		gain_tx (float): The antenna gain of the transmitter (dBi)
		wavelength (float): The wavelength of the signal

	Returns:
		The distance between the receiver and transmitter
	"""
	exp: float = (power_rx - power_tx - gain_rx - gain_tx) / 20
	denom: float = 4 * math.pi * (10**exp)
	return wavelength / denom

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("-pr", "--power-rx", type=float, required=True, help="Signal power of Rx (dBm)")
	parser.add_argument("-pt", "--power-tx", type=float, required=True, help="Signal power of Tx (dBm)")
	parser.add_argument("-gr", "--gain-rx", type=float, required=True, help="Antenna gain of Rx (dBi)")
	parser.add_argument("-gt", "--gain-tx", type=float, required=True, help="Antenna gain of Tx (dBi)")
	parser.add_argument("-wl", "--power-rx", type=float, required=True, help="Signal wavelength. Output distance will be the same distance units as this")
	args = parser.parse_args()

	distance: float = distance_form(args.pr, args.pt, args.gr, args.gt, args.wl)
	print(distance, file=sys.stdout) # output radius in same units as wavelength

if __name__ == "__main__":
	main()