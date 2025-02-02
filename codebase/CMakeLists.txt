###############################################################
#
# Top-level CMakeLists file for lrose-core
#
# dir: lrose-core/codebase
#
# written by script createCMakeLists.py
#
###############################################################

cmake_minimum_required(VERSION 3.0)

project (lrose-core)

# set policy CMP0100 so that AUTOMOC finds .hh files
if(${CMAKE_VERSION} VERSION_GREATER "3.17.0")
  cmake_policy(SET CMP0100 NEW)
endif()
if(${CMAKE_VERSION} VERSION_GREATER "3.10.0")
  cmake_policy(SET CMP0071 NEW)
endif()

set(CMAKE_C_COMPILER_NAMES clang gcc icc cc fcc)
set(CMAKE_CXX_COMPILER_NAMES clang++ g++ icpc c++ cxx FCC CC)

set(CMAKE_VERBOSE_MAKEFILE OFF)

SET(CMAKE_MODULE_PATH "${CMAKE_SOURCE_DIR}/../build/cmake/"
     CACHE INTERNAL "Location of our custom CMake modules.")

SET(CMAKE_PREFIX_PATH "${CMAKE_CURRENT_SOURCE_DIR}/build/cmake")

set(FETCHCONTENT_QUIET false CACHE BOOL "" FORCE)

set(PACKAGE "LROSE-CORE" CACHE STRING "")

# Finding pkg-config
find_package(PkgConfig REQUIRED)

# Finding Qt on mac OSX

if(APPLE)
find_path(Qt5_DIR NAMES Qt5Config.cmake qt5-config.cmake HINTS /usr/local/Cellar/qt@5/*/lib/cmake/Qt5 NO_DEFAULT_PATH)
endif(APPLE)
find_package (X11)
if (DEFINED X11_X11_LIB)
  get_filename_component(X11_LIB_DIR ${X11_X11_LIB} DIRECTORY)
endif()
find_package (HDF5)
find_package (NETCDF)
if (DEFINED HDF5_hdf5_LIBRARY_RELEASE)
  get_filename_component(HDF5_INSTALL_PREFIX ${HDF5_hdf5_LIBRARY_RELEASE} DIRECTORY)
endif()
if (NOT IS_DIRECTORY netCDF_INSTALL_PREFIX)
  set (netCDF_INSTALL_PREFIX ${CMAKE_INSTALL_PREFIX})
endif()
if (NOT IS_DIRECTORY HDF5_INSTALL_PREFIX)
  set (HDF5_INSTALL_PREFIX ${CMAKE_INSTALL_PREFIX})
endif()
if (NOT IS_DIRECTORY HDF5_C_INCLUDE_DIR)
  set (HDF5_C_INCLUDE_DIR ${CMAKE_INSTALL_PREFIX}/include)
endif()
message("X11_X11_INCLUDE_PATH: ${X11_X11_INCLUDE_PATH}")
message("X11_LIB_DIR: ${X11_LIB_DIR}")
message("HDF5_INSTALL_PREFIX: ${HDF5_INSTALL_PREFIX}")
message("HDF5_C_INCLUDE_DIR: ${HDF5_C_INCLUDE_DIR}")

# If user did not provide CMAKE_INSTALL_PREFIX, use ~/lrose
if(CMAKE_INSTALL_PREFIX_INITIALIZED_TO_DEFAULT)
  set(CMAKE_INSTALL_PREFIX "$ENV{HOME}/lrose" CACHE PATH "..." FORCE)
endif()
message("CMAKE_INSTALL_PREFIX is ${CMAKE_INSTALL_PREFIX}")

# Function for creating TDRP Params.cc and Params.hh files

function(makeTdrpParams)

# Add a custom generator for TDRP Params.cc and Params.hh files
# from their associated paramdef.<app> file

set(TDRP_EXECUTABLE ${CMAKE_INSTALL_PREFIX}/bin/tdrp_gen)
#find_program(TDRP_EXECUTABLE NAMES tdrp_gen PATHS ${CMAKE_INSTALL_PREFIX} /usr/local/lrose PATH_SUFFIXES bin)

add_custom_command (
OUTPUT ${CMAKE_CURRENT_SOURCE_DIR}/Params.hh ${CMAKE_CURRENT_SOURCE_DIR}/Params.cc
DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/paramdef.${PROJECT_NAME}
COMMAND cd ${CMAKE_CURRENT_SOURCE_DIR} && ${TDRP_EXECUTABLE}
-c++
-f paramdef.${PROJECT_NAME}
-prog ${PROJECT_NAME}
-add_ncar_copyright
COMMENT "Generating/updating Params.hh and Params.cc for ${PROJECT_NAME}"
)

endFunction()

enable_testing()

set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -fPIC ")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fPIC -std=c++11 ")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -DNO_JASPER_LIB ")

# Set RPATH so that executablefinds lrose libraries without needing LD_LIBRARY_PATH

set(CMAKE_SKIP_BUILD_RPATH FALSE)
set(CMAKE_BUILD_WITH_INSTALL_RPATH TRUE)

set(CMAKE_INSTALL_RPATH ${CMAKE_INSTALL_PREFIX}/lib)
set(CMAKE_INSTALL_RPATH_USE_LINK_PATH TRUE)

if(${CMAKE_SYSTEM_NAME} MATCHES "Linux")
  set(CMAKE_EXE_LINKER_FLAGS "-Wl,--enable-new-dtags")
endif()

add_subdirectory(libs)
add_subdirectory(apps)

