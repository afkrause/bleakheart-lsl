from bleak import BleakScanner, BleakClient
import asyncio
import bleakheart as bh
from bleakheart import HeartRate, PolarMeasurementData
import numpy as np
from os import sys
from pylsl import StreamInfo, StreamOutlet 

# to run asyncio scripts within spyder
#import nest_asyncio
#nest_asyncio.apply()

import signal
stop_running = False
def signal_handler(sig, frame):
    global stop_running
    print('You pressed Ctrl+C! Stopping and cleaning up.')
    stop_running = True



########## LSL stuff ######################
## For Polar H10  sampling frequency ##
# https://www.researchgate.net/post/What_is_the_sampling_rate_of_the_Polar_H10
# https://github.com/polarofficial/polar-ble-sdk
ECG_SAMPLING_FREQ = 130
ECG_CHUNKSIZE = 73 # transmission chunk size, should be (approximately?) the same as the number of ECG-samples per buffer / block sent by Polar H10
ACC_SAMPLING_FREQ = 25
ACC_CHUNKSIZE = 36 # transmission chunk size
OUTLET = []

HR_SAMPLING_FREQ = 1 # TODO: what is the sampling rate???
                
def create_ecg_lsl_outlet(stream_name):
    info = StreamInfo(stream_name, 'ECG', 1, ECG_SAMPLING_FREQ, 'float32')#, 'myuid2424')
    '''
    info.desc().append_child_value("manufacturer", "Polar")
    channels = info.desc().append_child("channels")
    channels.append_child("channel")\
        .append_child_value("name", 'ECG')\
        .append_child_value("unit", "microvolts")\
        .append_child_value("type", "ECG")
    '''
    return StreamOutlet(info, chunk_size = ECG_CHUNKSIZE)

def create_acc_lsl_outlet(stream_name):
    info = StreamInfo(stream_name, 'ACC', 3, ACC_SAMPLING_FREQ, 'float32')#, 'myuid2425')
    '''
    info.desc().append_child_value("manufacturer", "Polar")
    channels = info.desc().append_child("channels")    
    channels.append_child("channel")\
        .append_child_value("name", 'ACC')\
        .append_child_value("unit", "milli-g")\
        .append_child_value("type", "ACC")
    '''
    return StreamOutlet(info, chunk_size = ACC_CHUNKSIZE)


def create_heartrate_lsl_outlet(stream_name):
    info = StreamInfo(stream_name, 'HR', 2, HR_SAMPLING_FREQ, 'float32')#, 'myuid2426')
    '''
    info.desc().append_child_value("manufacturer", "Polar")
    channels = info.desc().append_child("channels")
    channels.append_child("channel")\
        .append_child_value("name", "HR")\
        .append_child_value("unit", "bpm")\
        .append_child_value("type", "HR")
    '''
    return StreamOutlet(info, chunk_size = 1)




# change these two parameters and see what happens.
# INSTANT_RATE is unsupported when UNPACK is False
UNPACK = True
INSTANT_RATE = UNPACK and False

async def find_device(name = "polar"):
    ## Find your sensor and connect to it
    # edit this line if you have another compatible sensor
    device_filter = lambda dev, adv: dev.name and name in dev.name.lower()
    device = await BleakScanner.find_device_by_filter(device_filter)
    if device==None: 
        sys.exit("Polar device not found")
        
    client = BleakClient(device)
    await client.connect()
    if not client.is_connected:
        sys.exit("Connection failed")
    else:
        print(f"Connected to {device.name}")
        return client

# stream 
async def stream(client):      
    pass


# just prints the details of what is shown on-screen
def print_hr_info():
    if UNPACK:
        print("   ('HR', tstamp, (bpm, rr_interval), energy)")
    else:
        print("   ('HR', tstamp, (bpm, [rr1,rr2,...]), energy)")
    print("where tstamp is in ns, rr intervals are in ms, and")
    print("energy expenditure (if present) is in kJoule.")    

def print_accel_info():
    print("After connecting, will print accelerometer data in the form")
    print(" ('ACC', tstamp, [(x1,y1,z1),(x2,y2,z2),...,(xn,yn,zn)])")
    print("where samples (xi, yi, zi) are in milli-g, tstamp is in ns")
    print("and it refers to the last sample (xn,yn,zn).")
    

def heartrate_callback(data):
    global lsl_hr_outlet
    """ This callback is sent the heart rate data and does all the 
    processing. You should ensure it returns before the next 
    frame is received from the sensor. 

    In this example, we simply print decoded heart rate data as it 
    is received """
    stream_type = data[0]
    timestamp = data[1] # the timestamp refers to the last sample!
    samples = np.array(data[2])    
    if stream_type == 'HR':
        print('(HR, RR-interval)=', samples)
        lsl_hr_outlet.push_sample(samples)
    

def callback(data):
    global lsl_ecg_outlet
    global lsl_acc_outlet
    """ This callback is sent the ECG and acceleration data and does all the 
    processing. You should ensure it returns before the next 
    frame is received from the sensor. 

    In this example, we simply print decoded acceleration data as it 
    is received """
    #print("len of ACC data = ", len(data[0]))
    #print(np.mean(np.array(data[0])))
    stream_type = data[0]
    timestamp = data[1] # the timestamp refers to the last sample!
    samples = np.array(data[2], dtype=np.float32)
    # print(len(samples))
    if stream_type == 'ACC':
        print("acc samples, mean accel (x,y,z) = ", len(samples), np.mean(samples, axis = 0))
        lsl_acc_outlet.push_chunk(samples)
    
    # TODO: how to add the timestamps ????
    if stream_type == 'ECG':
        print("ecg samples, mean ecg = ", len(samples), np.mean(np.array(samples)))
        lsl_ecg_outlet.push_chunk(samples)
    
# print some sensor status infos and capabilities
async def print_sensor_details(client):
    batterylevel = await bh.BatteryLevel(client).read()
    print("polar H10 battery level:", batterylevel)

    pmd = PolarMeasurementData(client)
    meas = await pmd.available_measurements()
    print("Measurements supported by Polar device:")
    print(meas)
    
    # ask about ACC settings
    settings=await pmd.available_settings('ACC')
    print("Request for available ACC settings returned the following:")
    for k,v in settings.items():
        print(f"{k}: {v}")    
        
    # ask about ECG settings
    settings=await pmd.available_settings('ECG')
    print("Request for available ECG settings returned the following:")
    for k,v in settings.items():
        print(f"{k}:\t{v}")        

async def main():
    global stop_running
    global lsl_hr_outlet
    global lsl_acc_outlet
    global lsl_ecg_outlet
    print("searching for Polar H10 breast belt sensor...")
    client = await find_device()
    '''
    task = asyncio.create_task(find_device())
    # print a basic waiting animation using dots
    while True:
        print(".",end="")
        await asyncio.sleep(0.5)
        if task.done():
            break
    # get the task result (the client object)
    client = task.result()
    #'''
    
    await print_sensor_details(client)

    #print_hr_info()
    #print_accel_info()

    #'''
    #polarh10_
    lsl_hr_outlet = create_heartrate_lsl_outlet("polarh10_hr")
    lsl_acc_outlet = create_acc_lsl_outlet("polarh10_acc")
    lsl_ecg_outlet = create_ecg_lsl_outlet("polarh10_ecg")
    
    pmd = PolarMeasurementData(client, callback=callback)

    err_code, err_msg, _ = await pmd.start_streaming('ACC', RANGE=2, SAMPLE_RATE=ACC_SAMPLING_FREQ)
    if err_code!=0:
        sys.exit(f"PMD returned an error: {err_msg}")        

    err_code, err_msg, _ = await pmd.start_streaming('ECG')
    if err_code!=0:
        sys.exit(f"PMD returned an error: {err_msg}")        
    #'''

    #'''
    heartrate=HeartRate(client, callback=heartrate_callback,
                            instant_rate=INSTANT_RATE,
                            unpack=UNPACK)
    await heartrate.start_notify()
    #'''
    
    

    # run forever    
    while True:
        await asyncio.sleep(0.5)
        if stop_running == True:
            break
    
    await heartrate.stop_notify()
    await pmd.stop_streaming('ACC')
    await pmd.stop_streaming('ECG')
    await client.disconnect()
        
if __name__ == "__main__":
    print("searching von PolarH10 (AIS-Lab Sensor ID: 0CDD543C; MAC=24:AC:AC:0C:DD:54")
    # add signal handler to capture a Ctrl+C signal
    print("press Ctrl+C to stop streaming.")
    signal.signal(signal.SIGINT, signal_handler)
    asyncio.run(main())
    print("cleanup done. exit.")
