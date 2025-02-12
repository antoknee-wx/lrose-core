# Build LROSE automatically using cmake - LINUX and MAC

1. [overview](#overview)
2. [prepare](#prepare)
3. [build](#build)
4. [verify](#verify)

<a name="overview"/>

## 1. Overview

Here we document the most autonomous way to perform the build.

We do this by checking out the build scripts from the bootstrap repository.

The lrose-core is checked out and built in /tmp.

Only the libraries and binaries are installed permanently.

The source code is in /tmp and is not permament.

The default install prefix is ```~/lrose```.

The default directories for installation are:

```
  ~/lrose/include
  ~/lrose/lib
  ~/lrose/bin
```

This can be changed using the ```--prefix``` argument on the scripts.

<a name="prepare"/>

## 2. Prepare

### Create a working directory for cloning:

```
  mkdir -p ~/git
  cd ~/git
```

### Install required packages

See:

* [lrose-core package dependencies](./lrose_package_dependencies.md)

<a name="build"/>

## 3. Build automatically using scripts in the bootstrap repository

### Clone the bootstrap for LROSE

```
  cd ~/git
  git clone https://github.com/ncar/lrose-bootstrap
```

The distribution will be in the lrose-bootstrap subdirectory:

```
  cd ~/git/lrose-bootstrap
```

### Run the ```checkout_and_build_cmake.py``` script:

To see the usage:

```
  cd ~/git/lrose-bootstrap/scripts
  ./checkout_and_build_cmake.py --help
```

```
  Usage: checkout_and_build_cmake.py [options]
  Options:
    -h, --help            show this help message and exit
    --clean               Cleanup tmp build dir
    --debug               Set debugging on
    --verbose             Set verbose debugging on
    --package=PACKAGE     Package name. Options are: lrose-core (default),
                          lrose-radx, lrose-cidd, samurai
    --releaseDate=RELEASEDATE
                          Date from which to compute tag for git clone. Applies
                          if --tag is not used.
    --tag=TAG             Tag to check out lrose. Overrides --releaseDate
    --prefix=PREFIX       Install directory, default: ~/lrose
    --buildDir=BUILDDIR   Temporary build dir, default: /tmp/lrose-build
    --logDir=LOGDIR       Logging dir, default: /tmp/lrose-build/logs
    --static              use static linking, default is dynamic
    --noScripts           Do not install runtime scripts as well as binaries
    --buildNetcdf         Build netcdf and hdf5 from source
    --fractl              Checkout and build fractl after core build is complete
    --vortrac             Checkout and build vortrac after core build is
                          complete
    --samurai             Checkout and build samurai after core build is
                          complete
    --cmake3              Use cmake3 instead of cmake for samurai
    --no_core_apps        Do not build the lrose core apps
    --withJasper          Set if jasper library is installed. This provides
                          support for jpeg compression in grib files.
    --verboseMake         Verbose output for make, default is summary
```

For most cases, the defaults work well.

For MAC OSX, static builds are forced.

`package` defaults to `lrose-core`.

Available packages are:

```
  lrose-core lrose-cidd lrose-radx samurai
```

We recommend building the full core, unless you have specific limitations.

For older systems, such as centos7, you will need to use ```--cmake3```.

To build and install the full lrose package into ```~/lrose```:

```
  ./checkout_and_build_cmake.py
```

To specify the sub-package, e.g. lrose-radx:

```
  ./checkout_and_build_cmake.py --package lrose-radx
```

To set the install directory:

```
  ./checkout_and_build_cmake.py --prefix /my/install/dir
```

To cleanup between builds:

```
  ./checkout_and_build_cmake.py --clean
```

<a name="build-using-script"/>

<a name="verify"/>

## 4. Verify

As the build proceeds, the compile details will be saved to log files. The paths to these files are printed on in the terminal.

If the build fails, check the log files.

To see the build progress, use the ```--verbose``` option.

To see the full compile commands, use the ```--verbose``` and ```--verboseMake``` options.

If the build succeeds, test out some of the executables. Try the commands:

```
  ~/lrose/bin/RadxPrint -h
  ~/lrose/bin/RadxConvert -h
  ~/lrose/bin/Radx2Grid -h
  ~/lrose/bin/HawkEye
```

