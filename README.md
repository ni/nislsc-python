# nislsc-python

## About

The **nislsc** package allows you to develop instrumentation, acquisition, and control applications with NI Switch Load and Signal Conditioning (SLSC) devices in Python.
NI created and supports this package.

### Documentation

- TODO: Add documentation here.

### Implementation

The package is implemented in Python as an object-oriented wrapper around the NI-SLSC C API using the [ctypes](https://docs.python.org/3/library/ctypes.html) Python Library.

### Supported NI-SLSC Driver Versions

- TODO: List supported NI-SLSC Driver versions

### Operating System Support

**nislsc** supports Windows and Linux operating systems where the NI-SLSC driver is sipported. Refer to [NI Hardware and Operating System Compatibility](https://www.ni.com/r/hw-support) for which versions of the driver support your hardware on a given operating system.

### Python Version Support

**nislsc** supports CPython 3.9+ and PyPy3.

## Installation

- TODO: Insert installation instructions here.

## Getting Started

- TODO: Insert getting started documentation here.

## Python Examples

- TODO: Create Python Examples and document here.

## Usage

- TODO: Insert usage instructions here.

## Bugs / Feature Requests

To report a bug or submit a feature request, please use the [GitHub issues page](https://github.com/ni/nislsc-python/issues).

### Information to Include When Asking for Help

Please include **all** of the following information when opening an issue:

- Detailed steps on how to reproduce the problem and full traceback, if applicable.
- The Python version used:

    ```bash
    python -c "import sys; print(sys.version)"
    ```

- The version of the **nislsc** used:

    ```bash
    python -m pip list
    ```

- The version of the NI-DAQmx driver used. Follow [this KB article](http://digital.ni.com/express.nsf/bycode/ex8amn) to determine the version of NI-SLSC you have installed.
- The operating system and version, for example Windows 7, CentOS 7.2, ...

## License

**nislsc** is licensed under an MIT-style license (see [LICENSE](https://github.com/ni/nislsc-python/blob/master/LICENSE)). Other incorporated projects may be licensed under different licenses. All licenses allow for non-commercial and commercial use.
