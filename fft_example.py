import pylab as plt
import numpy as np
from scipy.fftpack import rfft, irfft, fftfreq

time   = np.linspace(0,10,200)
signal = np.cos(5*np.pi*time) + 5*np.cos(7*np.pi*time) + np.cos(9*np.pi*time)

W = fftfreq(signal.size, d=time[1]-time[0])
print(W)
f_signal = rfft(signal)
#print(f_signal)
# If our original signal time was in seconds, this is now in Hz    
cut_f_signal = f_signal.copy()
cut_f_signal[(W<6)] = 0
cut_f_signal[(W>8)] = 0
cut_f_sign = f_signal.copy()

aa = cut_f_sign[(W>6)]
ww = W[W>6]
aa = aa[(ww<8)]
ww = ww[(ww<8)]



peak = max(cut_f_signal)
f_value = W[cut_f_signal>=peak]

print(peak,f_value)
cut_signal = irfft(cut_f_signal)

plt.subplot(321)
plt.plot(time,signal)
plt.subplot(322)
plt.plot(W,f_signal)
plt.xlim(0,10)
plt.subplot(323)
plt.plot(W,cut_f_signal)
plt.xlim(0,10)
plt.subplot(324)
plt.plot(time,cut_signal)
plt.subplot(325)
plt.plot(ww,aa)
plt.show()