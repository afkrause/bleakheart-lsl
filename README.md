
# bleakheart-lsl - steams Polar H10 sensor data via LSL

what is streamed: 
* Electrocardiogram (ECG in micro-Volts (µV)
* accelerometer data (ACC in milli-g)
* heart rate (HR in beats-per-minute (bpm))
* RR interval (in milli-seconds (ms))


The streams can be recorded using LabRecorder.
There is a script that can load recorded files and visualize the data ( visualize.py ).

## Install LabRecorder

To record LSL streams, use the LabRecorder Tool. 

### Linux Mint 22.3

Dependency: 

```bash
sudo apt install liblsl
```

this installs liblsl version 1.16.2-noble. 

Now install the matching LabRecorder Version 1.16:

https://github.com/labstreaminglayer/App-LabRecorder/releases/tag/v1.16.5



## Tips & Tricks

* under Linux Mint, *disable the firewall* to see the available streams, or create appropriate firewall rules.
* polarh10 python script: wait a bit until the accelerometer- and ecg data appears. heartrate is available first.
* bluetooth: disable and re-enable bluetooth if the polarh10 sensor is not found by the script.
* if bluetooth does not work, restart. the bluetooth stack is a bit unstable. 


