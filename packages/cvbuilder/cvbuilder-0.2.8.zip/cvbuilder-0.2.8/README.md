# OpenCV Hands-Free

**Unofficial** OpenCV builder for Python.

This package aims at building OpenCV with Python bindings from the official sources.
It provides a simple command line interface for starting the process of downloading the
official sources, configuring the build dependencies, compiling and installing the resulting
CV2 shared object within a virtual environment.

In contrast to [opencv-python](https://github.com/skvark/opencv-python) it will not provide any
wheels and therefore the installation / build process will be by far slower (depending on the
actual system performance).

**IMPORTANT NOTE**

Depending on the usage and system dependencies, the on-the-fly build output can
contain video and GUI functionality and the contrib package.


## Features

* builds against Python >= 3.4
* runs and builds inside virtual environment
* includes video support
* supports OpenCV check (import, build information)
* compiles with many flags enabled (which???)

## Supported OS

* Debian Jessie, Stretch
* Ubuntu 16.04
* LinuxMint 18.2
* Manjaro
* Arch
* Raspbian 9 (Stretch)


## Supported Python runtimes

* CPython 3.4, 3.5, 3.6
* PyPy (not yet)

**Note:** PyPy (5.10) is not supported yet due to missing path variables in module `sysconfig`.

## Installation

1. Use a Python's [virtual environment](https://docs.python.org/3/library/venv.html)
or even better install the package via [pipenv](https://docs.pipenv.org/): `pipenv install cvbuilder`
1. Follow instructions below


## Usage

After installing the package via pip / pipenv, you can manually invoke `cvbuilder` commands.

### Install system dependencies

```bash
cvbuilder system --enable-gui --enable-video
```

### Download, configure, build, install

The `do-it-all` command is:

```bash
cvbuilder build
```

or if you already downloaded the source zip files in the default temporary
directory or need to rerun the process in a clean way:

```bash
cvbuilder build --clean
```


## Custom

If you need to run the individual steps (i.e. for debugging) the following
commands are provided.

### Download sources

```bash
cvbuilder download
```

### Generate make config

```bash
cvbuilder configure [--tmpdir XYZ]
```

### Compile

```bash
cvbuilder make
```

### Install

```bash
cvbuilder install
```

### Dump

```bash
cvbuilder dump
```

### Check

You can run the check command:

```bash
cvbuilder check
``` 

in order to check whether the build process and installation worked.


# Running OpenCV

Now everything should be up and running and you should be able to work with OpenCV:

1. Start a python REPL: `pipenv run python`
1. Import the CV package: `import cv2`
1. Read [OpenCV documentation](http://docs.opencv.org/>)
