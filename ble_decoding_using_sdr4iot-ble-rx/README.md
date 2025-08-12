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

TIPP: When you open the file gr_ble.grc in GNU Radio Companion and save the graph, the file gr_ble.py
that is edited in the following is regenerated! This means, this section tells you to edit a generated
file! That is never a good idea but there is no way around it!

/dev/null is a Linux file. A platform independent variant of that file is available using os.devnull
In order to make the script run on Microsoft Windows, we need to use a platform independent version.

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

When the graph is executed, you actually execute a python script! The original GNU Radio Companion
graph is contained in the sdr4iot-ble-rx repository! The file is located here: sdr4iot-ble-rx\grc\gr_ble.grc
You can open this file in GNU Radio Companion (grc) 3.10.12.0 (Python 3.12.9) for example. 

Once you generate the flowgraph (MenuBar > Box with an triangle below it pointing downwards), the gr_ble.grc graph
is converted into the python script gr_ble.py. This script contains blocks that can be imported into other python
scripts. The gr_dump.py python script makes use of the gr_ble.py by importing it first:

```
from grc.gr_ble import gr_ble as gr_block
```

The graph starts with the RTL-SDR source configured to use a Hack-RF and scanning the frequency 2.426 Ghz.
With 10 Million Samples Per Second. Then it uses a https://wiki.gnuradio.org/index.php/Head block.
A head block is configured with a number that is the number of packets it passes on before it stops
transmitting packets downstream. This means it is purely used for limiting the amount of data that flows
through the system in order to not completely fill the harddrive with huge files for example!

Looking at the graph, the data flows from left to right and enters a ZMQ (Zero MQ, High Performance Message Queuing for Python)
sink. The sink opens up a socket on localhost and port 55555. (tcp://127.0.0.1:55555)
The sdr-dump.py python script from the sdr4iot-ble-rx repository, first executes the grc graph
and then connects to that socket and port. 

The sdr-dump.py script reads records from the socket. 
For each record, it first extracts the BLE Access Address.
Then it performs deswhitening on the BLE header.
It checks the PLDU type and retrieves the packet length.
It then performs dewithening on the rest of the BLE packet
and verifes the checksum.

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
python ./ble_dump.py -o tmp/dump1.pcap --iq-output=tmp/iq_output.dat
```

A few bits of information for the ble_dump.py script:
DO NOT NAME THE --iq-output file .csv! USE ANY OTHER EXTENSION. THE REASON IS, ble_dump.py WILL CREATE A .csv FILE ITSELF AUTOMATICALLY!
The ble_dump script will reuse the name of the --iq-output file and add
the .csv extension to the file and then create that .csv file.
It will enter some statistics data into the .csv file.
One very important piece of information is, where within the IQ-Data
a packet starts (Start_frame) and ends (End_frame). You can then easily point any decoder software
directly at those offsets into the IQ-Data file instead of decoding the entire IQ-Data file!

# Interpreting the output of sdr4iot-ble-rx

The command

```
cd C:\Users\lapto\dev\gnuradio\sdr4iot-ble-rx
python ./ble_dump.py -o tmp/dump1.pcap --iq-output=tmp/iq_output.dat
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

A great way to generate advertisement packets for sdr4iot-ble-rx to pick up
is to install the Android app called nRF Connect. 
Switch to the ADVERTISER tab and start the advertiser.
The advertiser will blast all advertisement channels with packets advertising
your phone. sdr4iot-ble-rx will capture these packets within seconds. That
way, the iq_output.csv file stays relatively small. I managed to capture
four advertisement packets and the iq_output.csv file has been 400 MB.


# Understanding the GNU Radio Source Code

C:\Users\lapto\dev\gnuradio\docs\usage-manual\(exported from wiki) Handling Flowgraphs.txt


# Understanding the implementation of the GSFK Mod and Demod blocks.

Both block are defined within the same .py file: gr-digital\python\digital\gfsk.py

Both are hiearchical blocks. https://wiki.gnuradio.org/index.php/Hier_Blocks_and_Parameters
A hierarchical block combines existing functionality into a new block.

In python, the Mod and Demod classes derive from the hier-class:

```
class gfsk_mod(gr.hier_block2):

...

class gfsk_demod(gr.hier_block2):

...
```

The __init__() function is the constructor. The parameters to the constructor will 
show in the GNU Radio Companion GUI dialog, when you double click the node.

First, the constructor of the parent class is called.

```
gr.hier_block2.__init__(self, "gfsk_mod",
						# Input signature
						gr.io_signature(1, 1, gr.sizeof_char),
						gr.io_signature(1, 1, gr.sizeof_gr_complex))  # Output signature
```

After that, the code inside __init__() assigns the parameters to member variables.

To understand the rest of the code, we first take a look at the bottom of the __init__() function.

```
# Connect & Initialize base class
if do_unpack:
	self.unpack = blocks.packed_to_unpacked_bb(1, gr.GR_MSB_FIRST)
	self.connect(self, self.unpack, self.nrz,
				 self.gaussian_filter, self.fmmod, self.amp, self)
else:
	self.connect(self, self.nrz, self.gaussian_filter,
				 self.fmmod, self.amp, self)
```

Because Mod and Demod are derived from hier_block2, they can call the connect() method.
This connect method takes a set of objects that will connected to each other in line which
forms the content of the hierarchical block.

We can see that the sequence consists of:

1. self
1. self.unpack
1. self.nrz
1. self.gaussian_filter
1. self.fmmod
1. self.amp
1. self

The first and last nodes are the class itself (self). 
In between there is unpack, nrz, gaussian_filter, fmmod and amp.

The code in the middle of the __init__() function creates the middle
nodes in the chain above.

The next question is, where is the code for unpack, nrz, ... and the rest?