# Introduction

The basic purpose of this test is to decode Bluetooth Low Energy advertisement packets using a HackRF One or similar Software Defined Radio and gnuradio. This repository does not use the GNURadio Companion GUI but it executes a Python script on the command line. The solution works on Microsoft Windows 11.

The original repository for sdr4iot-ble-rx is located here: https://github.com/Rtone/sdr4iot-ble-rx
The original repository is created for gnuradio 3.7. Since gnuradio 3.7 is deprecated, the original repository is not of great use any more.

An up-to-date version is contained here: https://github.com/oldprogram/sdr4iot-ble-rx
The updated fork works for gnuradio 3.10 on Microsoft Windows!

# How to run the application 

1. Clone the repository

```
git clone https://github.com/oldprogram/sdr4iot-ble-rx
```

2. Install gnuradio and a working python environment by installing radioconda on Microsoft Windows.
The homepage is https://github.com/ryanvolz/radioconda
Search for Releases and go to the Releases page.
On the Releases page select the newest release, scroll down to the Assets and click on "Show all xy assets".
In the unfolded list, select "radioconda-2025.03.14-Windows-x86_64.exe", download the .exe installer file
and run the installer.

# Necessary changes

As the python scripts have been developed on Linux, some changes are required to make them run in a Microsoft Windows environment.

## Replace the /dev/null file by os.devnull

/dev/null is a Linux file. A platform independent variant of that file is available using os.devnull

Edit gr_ble.py and add an import for os

```
import os
```

Replace the line

```
self.iq_output = iq_output = "/dev/null"
```

by

```
self.iq_output = iq_output = os.devnull
```

# Now install radioconda and the sdr4iot-ble-rx dependencies

The trick is to install gnuradio on windows using radioconda.
Since gnuradio is tightly coupled with python, you always need python to run gnuradio scripts anyways.
GNU Radio Companion (GRC) is a GUI which lets you define graphs that are compiled to python scripts.
When the graph is executed, you actually execute a python script!
radioconda seems to be a packaged python environment including gnuradio and the required python libraries.

I do actually not understand what radioconda really is but once installed, your
Windows start menu contains the application "radioconda Prompt".
The radioconda Prompt is a command line window which contains a python environment
with all packages for gnuradio!

Once the radioconda Prompt is opened, first install the required python packages for
sdr4iot-ble-rx

```
pip install zmq
pip install numpy
```

Plug in your SDR. I tested it using a HackRF One but it works with many SDRs.
The script will automatically detect your SDR, at least it detected and used my HackRF One
without me configuring any settings or providing any command line parameters.

You can then execute the python script within radioconda Prompt. 

```
cd C:\Users\lapto\dev\gnuradio\sdr4iot-ble-rx
python ./ble_dump.py -o tmp/dump1.pcap --iq-output tmp/iq_output.csv
```

# Interpreting the output of sdr4iot-ble-rx

The command

```
cd C:\Users\lapto\dev\gnuradio\sdr4iot-ble-rx
python ./ble_dump.py -o tmp/dump1.pcap --iq-output tmp/iq_output.csv
```

executes the python script. The python script starts to capture incoming
advertisement packets on the first advertisement channel 37. After a certain
amount of time it will switch to the next advertisement channel and capture
packets there. This means, you should let the applicatio run for a couple of
seconds before stopping it. If you stop it too early, it will probably not 
have the chance to capture any packets.

Be warned, the iq_output.csv is getting huge very, very quickly. I ran the 
script for 30 seconds which resulted in a 2 GB iq_output.csv file!

The script creates a subfolder called tmp acording to the command line parameters
given above. Within the tmp folder, there will be two files dump1.pcap and iq_output.csv.

The dump1.pcap file can be opened using Wireshark. Wireshark is a GUI which 
can decode packages from many communication protocols including Bluetooth.

A great way to generate advertisement packets is to install the Android app 
called nRF Connect. Switch to the ADVERTISER tab and start the advertiser.
The advertiser will blast all advertisement channels with packets advertising
your phone. sdr4iot-ble-rx will capture these packets within seconds. That
way, the iq_output.csv file stays relatively small. I managed to capture
four advertisement packets and the iq_output.csv file has been 400 MB.
