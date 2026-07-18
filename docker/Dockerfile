FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    curl \
    git \
    cppcheck \
    build-essential \
    python3 \
    && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | sh

ENV PATH="/bin:${PATH}"

RUN arduino-cli core update-index
RUN arduino-cli core install arduino:avr