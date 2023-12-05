from __future__ import print_function, division, unicode_literals
import wave
import numpy as np
from pylab import*
#import matplotlib.pyplot as plt
from scipy.io import wavfile
import pyaudio
from pydub import AudioSegment
from pydub.playback import play
from get_filename import get_filename
import sys


def fft_dis(fname):
    sampFreq, snd = wavfile.read(fname)
    snd = snd / (2.**15) #convert sound array to float pt. values
    s1 = snd[:,0] #left channel
    s2 = snd[:,1] #right channel
    n = len(s1)
    p = fft(s1) # take the fourier transform of left channel
    m = len(s2) 
    p2 = fft(s2) # take the fourier transform of right channel
    nUniquePts = int(ceil((n+1)/2.0))
    p = p[0:nUniquePts]
    p = abs(p)
    mUniquePts = int(ceil((m+1)/2.0))
    p2 = p2[0:mUniquePts]
    p2 = abs(p2)
    p = p / float(n) # scale by the number of points so that
             # the magnitude does not depend on the length 
             # of the signal or on its sampling frequency  
    p = p**2  # square it to get the power 
# multiply by two (see technical document for details)
# odd nfft excludes Nyquist point
    if n % 2 > 0: # we've got odd number of points fft
        p[1:len(p)] = p[1:len(p)] * 2
    else:
        p[1:len(p) -1] = p[1:len(p) - 1] * 2 # we've got even number of points fft
    # freqArray = arange(0, nUniquePts, 1.0) * (sampFreq / n);
    # plt.plot(freqArray/1000, 10*log10(p), color='k')
    # plt.xlabel('Channel_Frequency (kHz)')
    # plt.ylabel('Channel_Power (dB)')
    # plt.show()
    
def voulume_changer(file_name, mode, scale):
    fo = file_name
    song = AudioSegment.from_wav(fo)
    if mode =='p':
        db = scale
        louder_song = song + db
    elif mode == 'm':
        db = scale
        louder_song = song - db   
    louder_song.export(fo, format='wav')

def compressed_audio(dir , fn, lowpass, highpass):
    fn = dir + fn
    file_name = get_filename(fn)
    wfin = wave.open(fn, 'rb')
    par = list(wfin.getparams())
    print("params wav audio: ") # Get the parameters from the input.
    # This file is stereo, 2 bytes/sample, 44.1 kHz.
    par[3] = 5 # The number of samples will be set by writeframes.
    # lowpass = 700 # Remove lower frequencies. #21 default
    # highpass = 14000 # Remove higher frequencies.#9000 default
    new_fn = dir+'filtered_'+str(file_name)+'_'+str(lowpass)+'lp_'+str(highpass)+'hp.wav'
    wfout = wave.open(new_fn, 'rb')  # Open the output file
    wfout.setparams(tuple(par)) # Use the same parameters as the input file.

    sz = wfin.getframerate() # Read and process 1 second at a time.
    c = int(wfin.getnframes()/sz) # whole file
    for num in range(c):
        print('Processing {}/{} s'.format(num+1, c))
        da = np.fromstring(wfin.readframes(sz), dtype=np.int16)
        left, right = da[0::2], da[1::2] # left and right channel
        lf, rf = np.fft.rfft(left), np.fft.rfft(right)
        lf[:lowpass], rf[:lowpass] = 0, 0 # low pass filter
        lf[55:66], rf[55:66] = 0, 0 # line noise
        lf[highpass:], rf[highpass:] = 0,0 # high pass filter
        nl, nr = np.fft.irfft(lf), np.fft.irfft(rf)
        ns = np.column_stack((nl,nr)).ravel().astype(np.int16)
        wfout.writeframes(ns.tostring())
    # Close the files.
    wfin.close()
    wfout.close()

    n = 0
    fo = new_fn
    for n in range (0,2): 
        if n==0:
            fft_dis(fn)
        elif n==1:
            fft_dis(fo)
    return fo
