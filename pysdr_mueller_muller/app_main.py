import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import math
import struct
import os

def main():
    print("tests")

    #samples = np.zeros(100 + 10, dtype=np.complex64)
    #samples[2] = 13 + 1*1j

    #plt.figure()
    #plt.plot(samples, '.-')
    #plt.show(block=False)

    ## this part came from pulse shaping exercise
    #num_symbols = 100
    #
    ##sps = 8
    sps = 2
    #bits = np.random.randint(0, 2, num_symbols) # Our data to be transmitted, 1's and 0's
    #
    ## draw a graph of the input data
    #plt.figure('in')
    #plt.plot(bits, '.-')
    #plt.show(block=False)

    #print('')
    #print("--input--");
    #for idx in range(len(bits)):
    #    if bits[idx].real > 0:
    #        print(1, end="")
    #    else:
    #        print(0, end="")
    #print('') # newline

    #pulse_train = np.array([])
    #for bit in bits:
    #    pulse = np.zeros(sps)
    #    pulse[0] = bit*2-1 # set the first value to either a 1 or -1
    #    pulse_train = np.concatenate((pulse_train, pulse)) # add the 8 samples to the signal

    #print(pulse_train)

    ## Create our raised-cosine filter
    #num_taps = 101
    #beta = 0.35
    #
    #Ts = sps # Assume sample rate is 1 Hz, so sample period is 1, so *symbol* period is 8
    #
    #t = np.arange(-51, 52) # remember it's not inclusive of final number
    #h = np.sinc(t/Ts) * np.cos(np.pi*beta*t/Ts) / (1 - (2*beta*t/Ts)**2)
    #
    ## Filter our signal, in order to apply the pulse shaping
    #samples = np.convolve(pulse_train, h)
    #print(samples)



    #for idx in range(len(samples)):
    #    if samples[idx].real > 0:
    #        print(1, end="")
    #    else:
    #        print(0, end="")
    #print('') # newline


    #plt.plot(samples, '.-')
    #plt.show()




    ## Create and apply fractional delay filter

    #N = 21 # number of taps
    #n = np.arange(-N//2, N//2) # ...-3,-2,-1,0,1,2,3...

    #delay = 0.4 # fractional delay, in samples
    #h = np.sinc(n - delay) # calc filter taps
    #h *= np.hamming(N) # window the filter to make sure it decays to 0 on both sides
    #h /= np.sum(h) # normalize to get unity gain, we don't want to change the amplitude/power

    #samples = np.convolve(samples, h) # apply filter





    # This does not work!
    # When the frequency offset is enabled, the M&M CDR
    # Mueller & Müller Clock and Data Recovery
    # does not work when Samples Per Symbol (SPS) is set to 2!

    ## apply a freq offset
    #fs = 1e6 # assume our sample rate is 1 MHz
    #fo = 13000 # simulate freq offset
    #Ts = 1/fs # calc sample period
    #t = np.arange(0, Ts*len(samples), Ts) # create time vector
    #samples = samples * np.exp(1j*2*np.pi*fo*t) # perform freq shift






    # read IQ data from file produced by a gnu-radio test-graph
    # This file contains real values after quadrature demodulation of
    # a GFSK Modulated packet
    # Read in file. We have to tell numpy what format it is
    #
    # The input data is created from a bit sequence: [000111011] which
    # is repeated for a total length of 120 bits
    samples = np.fromfile('quadrature_demod_output.data', np.float32)
    #print(samples)

    print("--input--");

    # draw a graph of the input
    plt.figure('input')
    plt.plot(samples, '.-')
    plt.show(block=False)

    mu = 0 # initial estimate of phase of sample
    out = np.zeros(len(samples) + 10, dtype=np.complex64)
    out_rail = np.zeros(len(samples) + 10, dtype=np.complex64) # stores values, each iteration we need the previous 2 values plus current value
    i_in = 0 # input samples index
    i_out = 2 # output index (let first two outputs be 0)
    while i_out < len(samples) and i_in+16 < len(samples):
        out[i_out] = samples[i_in] # grab what we think is the "best" sample
        out_rail[i_out] = int(np.real(out[i_out]) > 0) + 1j*int(np.imag(out[i_out]) > 0)
        x = (out_rail[i_out] - out_rail[i_out-2]) * np.conj(out[i_out-1])
        y = (out[i_out] - out[i_out-2]) * np.conj(out_rail[i_out-1])
        mm_val = np.real(y - x)
        mu += sps + 0.3*mm_val
        i_in += int(np.floor(mu)) # round down to nearest int since we are using it as an index
        mu = mu - np.floor(mu) # remove the integer part of mu
        i_out += 1 # increment output index
    out = out[2:i_out] # remove the first two, and anything after i_out (that was never filled out)

    #samples = out # only include this line if you want to connect this code snippet with the Costas Loop later on


    print("--output--");
    #type(out)


    #print(out)

    # convert recovered signal into bits and print the bits
    bits_out = np.array([])
    for idx in range(len(out)):
        if out[idx].real > 0:
            print(1, end="")
            bits_out = np.append(bits_out, 1)
        else:
            print(0, end="")
            bits_out = np.append(bits_out, 0)
    print('') # newline

    # draw a graph of the converted bits
    plt.figure('output')
    plt.plot(bits_out, '.-')
    plt.show(block=True)

    #plt.figure()
    #plt.plot(samples, '.-')
    #plt.show(block=False)

    #plt.figure()
    #plt.plot(out, '.-')
    #plt.show()

if __name__ == '__main__':
    main()