from pydub import AudioSegment
from numpy.random import uniform
import numpy as np
import sys

pitchShift = float(sys.argv[1])

# filename = 'output.wav'
# sound = AudioSegment.from_file(filename, format=filename[-3:])

# new_sample_rate = int(sound.frame_rate * (2.0 ** pitchShift))
# hipitch_sound = sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})
# hipitch_sound = hipitch_sound.set_frame_rate(48000)
# hipitch_sound.export(f"octave_{pitchShift}.wav", format="wav")

# octaves = 0.5
# for octaves in np.linspace(-1,1,21):
#     new_sample_rate = int(sound.frame_rate * (2.0 ** octaves))
#     hipitch_sound = sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})
#     hipitch_sound = hipitch_sound.set_frame_rate(44100)#export / save pitch changed sound
#     hipitch_sound.export(f"octave_{octaves}.wav", format="wav")



def stretch(sound_array, f, window_size, h):
    """ Stretches the sound by a factor `f` """
    print(window_size, f, h)

    phase  = np.zeros(window_size)
    hanning_window = np.hanning(window_size)
    result = np.zeros(int(len(sound_array) / f + window_size))

    for i in np.arange(0, len(sound_array)-(window_size+h), int(h*f)):

        # two potentially overlapping subarrays
        print(i)
        a1 = sound_array[i: i + window_size]
        a2 = sound_array[i + h: i + window_size + h]

        # resynchronize the second array on the first
        s1 =  np.fft.fft(hanning_window * a1)
        s2 =  np.fft.fft(hanning_window * a2)
        phase = (phase + np.angle(s2/s1)) % 2*np.pi
        a2_rephased = np.fft.ifft(np.abs(s2)*np.exp(1j*phase))

        # add to result
        i2 = int(i/f)
        result[i2 : i2 + window_size] += hanning_window*a2_rephased

    result = ((2**(16-4)) * result/result.max()) # normalize (16bit)

    return result.astype('int16')


def pitchshift(snd_array, n, window_size=2**13, h=2**11):
    """ Changes the pitch of a sound by ``n`` semitones. """
    factor = 2**(1.0 * n / 12.0)
    stretched = stretch(snd_array, 1.0/factor, window_size, h)
    return speedx(stretched[window_size:], factor)


from scipy.io import wavfile

fps, bowl_sound = wavfile.read("output.wav")
tones = range(-25,25)
transposed = [pitchshift(bowl_sound, n) for n in tones]
# transposed = [pitchshift(bowl_sound, n) for n in tones]
