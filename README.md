
# bleakheart-lsl - steams Polar H10 sensor data via LSL

what is streamed: 
* Electrocardiogram (ECG in micro-Volts (µV)
* accelerometer data (ACC in milli-g)
* heart rate (HR in beats-per-minute (bpm))
* RR interval (in milli-seconds (ms))


The streams can be recorded using LabRecorder.
There is a script that can load recorded files and visualize the data ( visualize.py ):

![Visualization](visualization.png)

## Install LabRecorder

To record LSL streams, use the LabRecorder Tool. 

### Linux Mint 22.3

LabRecorder needs a system-wide installed liblsl and depends on QT.

For Linux Mint 22.3, install LabRecorder 1.16, because the newer releases depend on a QT version not yet available in the Linux Mint repository.

* first install liblsl: https://github.com/sccn/liblsl/releases/download/v1.16.2/liblsl-1.16.2-noble_amd64.deb
* then install LabRecorder: https://github.com/labstreaminglayer/App-LabRecorder/releases/tag/v1.16.5



## Tips & Tricks

* under Linux Mint, *disable the firewall* to see the available streams, or create appropriate firewall rules.
* polarh10 python script: wait a bit until the accelerometer- and ecg data appears. heartrate is available first.
* bluetooth: disable and re-enable bluetooth if the polarh10 sensor is not found by the script.
* if bluetooth does not work, reboot Linux (Mint). The bluetooth stack is a bit unstable. 


## TODOS

visualize.py:
* the matplotlib plot function downsamples the ECG curve. zooming in shows less data than actually is available
* add slider to zoom vertically?
