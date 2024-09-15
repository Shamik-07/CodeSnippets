# creates a build time variable called image and assigns bullseye(Debian 11)
ARG IMAGE=bullseye

# base image of the docker container
FROM mcr.microsoft.com/devcontainers/${IMAGE}

# sets env variable to send the python output to the terminal without buffering, usefule for logging and debugging
ENV PYTHONUNBUFFERED 1

# debian frontend to non iteractive to avoid interactive prompts during package installation
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive

# installs postgre common; runs a script that sets up the postgre sql apt repo allwoing to install postgresql packages from the official repo
RUN apt-get -y install --no-install-recommends postgresql-common \
    && /usr/share/postgresql-common/pgdg/apt.postgresql.org.sh -y

# install postgre 16; cleans up the local repo of retrieved packages, removes the apt list files to free up space and reduce the image size
RUN apt-get -y install --no-install-recommends postgresql-client-16 \
    && apt-get clean -y && rm -rf /var/lib/apt/lists/*