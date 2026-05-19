
# bleakheart-lsl - steams Polar H10 sensor data via LSL

what is streamed: 
* Electrocardiogram (ECG in micro-Volts (µV)
* accelerometer data (ACC in milli-g)
* heart rate (HR in beats-per-minute (bpm))
* RR interval (in milli-seconds (ms))


The streams can be recorded using LabRecorder.
There is a script that can load recorded files and visualize the data ( visualize.py ).

## Install LabRecorder

To record LSL streams, use the LabRecorder Tool: 

### Linux Ubuntu

The Ubuntu releases do not typically ship with their dependencies, so you must download and install those:
* Download, extract, and install the latest [liblsl-{version}-{target}_amd64.deb from its release page](https://github.com/sccn/liblsl/releases)
    * We hope to make this available via a package manager soon.
      * Quick ref Ubuntu 24.04: `curl -L https://github.com/sccn/liblsl/releases/download/v1.17.4/liblsl-1.17.4-noble_amd64.deb -o liblsl.deb`
      * Quick ref Ubuntu 22.04: `curl -L https://github.com/sccn/liblsl/releases/download/v1.17.4/liblsl-1.17.4-jammy_amd64.deb -o liblsl.deb`
    * You can install liblsl directly by double-clicking on the deb, or with `sudo dpkg -i {filename}.deb` or `sudo apt install {filename}.deb`
* See the bottom of the [lsl build env docs](https://labstreaminglayer.readthedocs.io/dev/build_env.html).
    * For most cases, this will amount to installing Qt and its dependencies:
      * Ubuntu >= 22.04: `sudo apt-get install qt6-base-dev freeglut3-dev`

## Tips & Tricks

* under Linux Mint, *disable the firewall* to see the available streams, or create appropriate firewall rules.
* polarh10 python script: wait a bit until the accelerometer- and ecg data appears. heartrate is available first.
* bluetooth: disable and re-enable bluetooth if the polarh10 sensor is not found by the script.
* if bluetooth does not work, restart. the bluetooth stack is a bit unstable. 


