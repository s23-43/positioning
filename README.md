# Positioning Algorithm for S23-43's Experimental Cellular Positioning System
This is Team S23-43's implementation of a positioning algorithm, which is just one part of our senior design project. Our objective is to design and build a positioning system that wirelessly tracks an object's location, taking advantage of cellular communications standards. Messages are sent over the air between software-defined radios on the object and on no fewer than 3 observation points (OPs). These wireless messages provide data to calculate path losses between the object and the OPs, which then allows a central computer to estimate the object's position with this in-house algorithm. This system would ideally be able to scale up to support tracing several objects in a large warehouse.

# Dependencies
## With Docker
If you decide to run the scripts in a Docker container, then the only necessary dependency is [Docker](https://www.docker.com/).
## Without Docker
While building a Docker image using the provided Dockerfile is recommended, it is not necessary. However, this project was made under the assumption it would be run on [Ubuntu 20.04 LTS](https://releases.ubuntu.com/focal/), so if the project is running on a different version of Ubuntu or a different OS, it may not work as expected.

Run the following commands on your instance of Ubuntu 20.04:
- `sudo apt install python3 python3-pip`
- `pip install --upgrade pip`
- `pip install sympy numpy`

Now you should be good to go!

# How to use
## Docker (optional)
1. `docker build -t <IMAGE_NAME> /path/to/repo`
2. `docker run --rm -v /path/to/repo:/app -it <IMAGE_NAME>`
3. The container should be running, and you should be in its terminal.