# enmon

**Environmental Monitoring Toolkit for HARDWARIO Bridge Module**

This project is a Python CLI tool providing access to HARDWARIO Bridge Module - an USB to I2C adapter. In connection with HARDWARIO Climate Module, this tool can provide useful environmental data - temperature, relative air humidity, atmospheric pressure, altitude above the sea level, and illuminance. The data can be output to console stdout or published via MQTT message in JSON format.


## Requirements

* macOS or Linux machine (e.g. Raspberry Pi)
* MicroUSB cable
* HARDWARIO Bridge Module
* HARDWARIO Climate Module


## Installation on Raspberry Pi

> Only the official Raspbian distribution is supported. The following procedure has been tested with Raspbian Buster Lite.

1. Install the build tools:

    sudo apt install -y autotools-dev autoconf automake libtool

1. Install the library dependencies:

    sudo apt install -y libudev-dev libusb-1.0-0-dev

1. Downloaded the sources:

    $ wget https://github.com/libusb/hidapi/archive/hidapi-0.9.0.tar.gz

1. Extract the downloaded sources:

    $ tar xzf hidapi-0.9.0.tar.gz

1. Go to the sources directory:

    $ cd hidapi-hidapi-0.9.0

1. Build the library:

    $ ./bootstrap
    $ ./configure
    $ make

1. Install the library:

    $ sudo make install

Alternatively, install the `hidapi` library as a package:

    $ sudo apt install -y libhidapi-libusb0

Install the Python tool from PyPI:

    $ sudo pip3 install enmon


## Installation on macOS

1. Downloaded the sources:

    $ git clone https://github.com/libusb/hidapi.git

1. Go to the sources directory:

    $ cd hidapi

1. Build the library:

    $ ./bootstrap
    $ ./configure
    $ make

1. Install the library:

    $ sudo make install


## Contributing

Please read [**CONTRIBUTING.md**](https://github.com/hardwario/enmon/blob/master/CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.


## Versioning

We use [**SemVer**](https://semver.org/) for versioning. For the versions available, see the [**tags on this repository**](https://github.com/hardwario/enmon/tags).


## Authors

* [**Pavel Hübner**](https://github.com/hubpav) - Initial work


## License

This project is licensed under the [**MIT License**](https://opensource.org/licenses/MIT/) - see the [**LICENSE**](https://github.com/hardwario/enmon/blob/master/LICENSE) file for details.
