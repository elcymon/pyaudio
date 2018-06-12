import sys
import pyaudio
import numpy as np
import time
import wave
exp_dur = 0
pause_t = 0
p = pyaudio.PyAudio()

def stream_sound(f,stream_length,volume):
    
    f_array = np.arange(490,f+1,1)
    fs = 44100       # sampling rate, Hz, must be integer
    #f =  700.0        # sine frequency, Hz, may be float

    # generate samples, note conversion to float32 array
    # f = f_array[0]
    samples = volume * (np.sin(2*np.pi*np.arange(fs*stream_length*4)*f/fs)).astype(np.float32)
    print max(samples)
    for f in f_array:
        print f
        samples += volume * (np.sin(2*np.pi*np.arange(fs*stream_length*4)*f/fs)).astype(np.float32)
    samples = np.array(samples,dtype=np.int16)
    # print samples
    # waveFile = wave.open('100hz-500hz-1hz.wav','wb')
    # waveFile.setnchannels(1)
    # waveFile.setsampwidth(p.get_sample_size(pyaudio.paFloat32))
    # waveFile.setframerate(fs)
    # waveFile.writeframes(b''.join(samples))
    # waveFile.close()
    send_to_speaker(samples,pyaudio.paFloat32,1,fs,True)
    # for paFloat32 sample values must be in range [-1.0, 1.0]
def send_to_speaker(samples,format,channels,rate,output):
    global p
    stream = p.open(format=format,
                    channels=channels,
                    rate=rate,
                    output=output)

    t = time.time()
    d = time.time() - t
    while d < exp_dur:
            
        # play. May repeat with different volume values (if done interactively)
        t1 = time.time()
        stream.write(samples)
        print('stream duration = ',time.time()-t1)
        t1 = time.time()
        if pause_t > 0:

            time.sleep(pause_t)
        print('pause time = ', time.time()-t1)

        d = round(time.time() - t)
        print(d,exp_dur)
    stream.stop_stream()
    stream.close()

    p.terminate()


if __name__ == '__main__':
    if len(sys.argv) == 6:
        print 'deprecated jor'
        a = sys.argv
        exp_dur = float(a[1])
        freq = float(a[2])
        stream_t = float(a[3])
        pause_t = float(a[4])
        vol = float(a[5])

        time.sleep(0)
        stream_sound(freq,stream_t,vol)
    elif len(sys.argv) == 4:
        exp_dur = float(sys.argv[1])
        pause_t = float(sys.argv[3])
        filename = sys.argv[2]
        f = wave.open(filename,'rb')
        samples = f.readframes(f.getnframes())
        format = p.get_format_from_width(f.getsampwidth())
        channels = f.getnchannels()
        rate = f.getframerate()
        output = True
        send_to_speaker(samples,format,channels,rate,output)
    else:
        print('''
                invalid start up
                usage:\n
                python audio_gen.py exp_dur freq stream_t pause_t vol\n\n''')
        