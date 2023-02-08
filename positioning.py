#!/usr/bin/env python3

import math

# Observation points have a 2D coordinate to represent position
class ObservationPoint:
	def __init__(self, x:float, y:float):
		self.x = x
		self.y = y

# Takes two 2D coords and returns the distance between them
def pythag(a:tuple[float, float], b:tuple[float, float]) -> float:
	dx = a[0] - b[0]
	dy = a[1] - b[1]
	return math.sqrt(dx**2 + dy**2)

def main():
	# TODO: Implement main function
	pass

if __name__ == "__main__":
	main()