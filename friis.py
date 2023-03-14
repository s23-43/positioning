#!/usr/bin/env python3

import argparse
import math
import sys

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("-pr", type=float, required=True, help="Signal power of Rx (dBm)")
	parser.add_argument("-pt", type=float, required=True, help="Signal power of Tx (dBm)")
	parser.add_argument("-gr", type=float, required=True, help="Antenna gain of Rx (dBi)")
	parser.add_argument("-gt", type=float, required=True, help="Antenna gain of Tx (dBi)")
	parser.add_argument("-wl", type=float, required=True, help="Signal wavelength")
	args = parser.parse_args()

	exp: float = (args.pr - args.pt - args.gt - args.gr) / 20
	r: float = args.wl / (4 * math.pi * (10**exp))

	print(r, file=sys.stdout) # output radius in same units as wavelength

if __name__ == "__main__":
	main()