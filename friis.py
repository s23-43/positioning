#!/usr/bin/env python3

import argparse
import math
import sys

def calculate_distance(power_rx: float, power_tx: float, gain_rx: float, gain_tx: float, wavelength: float) -> float:
	"""
	Calculates the distance between a receiver and a transmitter using the decibel form of the Friis transmission equation
	Friis transmission equation (conventional form):
		Pr[dBm] = Pt[dBm] + Gt[dBi] + Gr[dBi] + 20*log10(λ/(4πd))
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
	parser.add_argument("-pr", type=float, required=True, help="Signal power of Rx (dBm)")
	parser.add_argument("-pt", type=float, required=True, help="Signal power of Tx (dBm)")
	parser.add_argument("-gr", type=float, required=True, help="Antenna gain of Rx (dBi)")
	parser.add_argument("-gt", type=float, required=True, help="Antenna gain of Tx (dBi)")
	parser.add_argument("-wl", type=float, required=True, help="Signal wavelength. Output distance will be the same distance units as this")
	args = parser.parse_args()

	distance: float = calculate_distance(args.pr, args.pt, args.gr, args.gt, args.wl)
	print(distance, file=sys.stdout) # output radius in same units as wavelength

if __name__ == "__main__":
	main()