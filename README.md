# Positioning Algorithm for S23-43's Experimental 5G Positioning System
This code is written with the expectation that it will run on [Ubuntu 20.04 LTS](https://releases.ubuntu.com/focal/), so we have provided a Dockerfile with the necessary dependencies.

## Running the Docker container
1. `docker build -t <IMAGE_NAME> /path/to/repo`
2. `docker run --rm -v /path/to/repo:/app -it <IMAGE_NAME>`
3. The container should be running, and you should be in its terminal.

## Calculating a distance between a receiver and transmitter with the Friis transmission equation
TODO: Write instructions to calculate distance with `friis.py`

## Estimating a position with distances between receivers and transmitters
TODO: Write instructions to estimate position with `positioning.py`