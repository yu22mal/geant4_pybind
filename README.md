# Python bindings for Geant4

This is a fork project from the main one developed by [HaarigerHarald](https://github.com/HaarigerHarald). 
The aim of this project is to add optical physics support currently missing in the main one (as of January 2022).

Basic installation:

 1. Compile Geant4 with CMake option `GEANT4_BUILD_TLS_MODEL=global-dynamic`
 2. Setup Geant4 environment:
 ```
 source /path/to/geant4-v11.0.0/installation/bin/geant4.sh
 ```
 3. Clone and install `geant4_pybind`:
 ```
 git clone --recursive https://github.com/yu22mal/geant4_pybind
 pip3 install ./geant4_pybind
 ```

Complete instructions can be found on the page of the original project's page: [geant4_pybind](https://github.com/HaarigerHarald/geant4_pybind). 

