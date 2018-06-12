import pyaudio
import numpy as np
import time
p = pyaudio.PyAudio()

volume = 0.5     # range [0.0, 1.0]
fs = 44100       # sampling rate, Hz, must be integer
duration = 1.0   # in seconds, may be float
f =  700.0        # sine frequency, Hz, may be float

# generate samples, note conversion to float32 array
samples = (np.sin(2*np.pi*np.arange(fs*duration)*f/fs)).astype(np.float32)

f = 1700.0
samples2 = (np.sin(2*np.pi*np.arange(fs*duration)*f/fs)).astype(np.float32)

# for paFloat32 sample values must be in range [-1.0, 1.0]
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=fs,
                output=True)

# play. May repeat with different volume values (if done interactively)
t = time.time()
change = True
t2 = time.time()
cnt = 0
while True:
    cnt +=1
    T = time.time() - t2
    print(T,1/T)
    if time.time() - t > 10:
        change = not change
        t = time.time()
    if change:
        stream.write(samples)
    else:
        stream.write(samples2)
    t2 = time.time()

stream.stop_stream()
stream.close()

p.terminate()
