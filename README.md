# Positioning Algorithm for S23-43's Experimental 5G Positioning System
This code is written with the expectation that it will run on [Ubuntu 20.04 LTS](https://releases.ubuntu.com/focal/), so we have provided a Dockerfile with the necessary dependencies.

## Run Docker container (optional)
1. `docker build -t <IMAGE_NAME> /path/to/repo`
2. `docker run --rm -v /path/to/repo:/app -it <IMAGE_NAME>`
3. The container should be running, and you should be in its terminal.