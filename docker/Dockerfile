FROM ubuntu:22.04

RUN apt-get update && apt-get install -y curl python3

RUN curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | sh

ENV PATH="/bin:${PATH}"

RUN arduino-cli core update-index
RUN arduino-cli core install arduino:avr