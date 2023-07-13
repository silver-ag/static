import pyaudio
from scipy.io import wavfile
import numpy as np
import math

# globals

global_sample_widths = {1: np.int8, 2: np.int16, 3: np.int32, 4: np.int64}

# CLASSES

class StaticPlayer:
    def __init__(self, srate = 32000, swidth = 2):
        self.render_srate = srate
        self.render_swidth = swidth
        self.PA = pyaudio.PyAudio()
        self.PAStream = self.PA.open(format = self.PA.get_format_from_width(swidth, unsigned = False), channels = 1, rate = srate, output = True)
    def cleanup(self):
        self.PAStream.stop_stream()
        self.PAStream.close()
        self.PA.terminate()
    def play(self, sound):
        self.PAStream.write(sound.render_pcm(self.render_srate, self.render_swidth).tobytes())
    def save(self, sound, filename):
        sound.save(filename, self.render_srate, self.render_swidth)

class Sound:
    def __init__(self, f, l, memoised = True):
        self.f = f
        self.length = l
        self.memoised = memoised
        self._pcm = {}
    def render_pcm(self, srate, swidth):
        if self.memoised and (srate,swidth) in self._pcm:
            return self._pcm[(srate,swidth)]
        else:
            widthinfo = np.iinfo(global_sample_widths[swidth])
            total_samples = (int)(srate * self.length)
            pcm = np.zeros(total_samples, dtype=widthinfo.dtype)
            step = 1/srate
            for i in range(total_samples):
                # f(t) returns a value -1 to 1, convert to min-max for pcm data
                # (if min is not -max we want to just go to the maximum range that's centred on 0 so 0s are preserved)
                pcm[i] = (int)(self.f(i*step) * min(widthinfo.max, abs(widthinfo.min)))
            if self.memoised:
                self._pcm[(srate,swidth)] = pcm
            return pcm
    def save(self, filename, srate, swidth):
        pcm = self.render_pcm(srate, swidth)
        wavfile.write(filename, srate, pcm)
    def cut(self, start, length):
        # return a new sound that's a part cut out of this one
        return Sound(lambda t: self.f(t + start), length)
    @staticmethod
    def seq(*snds):
        sound_track = []
        cursor = 0
        for snd in snds:
            sound_track.append([cursor,cursor+snd.length,snd])
            cursor += snd.length
        def new_f(t):
            for start,end,snd in sound_track:
                if t >= start and t <= end:
                    return snd.f(t - start)
            raise(Exception('seq played to a point that shouldnt be possible'))
        return Sound(new_f, sum([snd.length for snd in snds]))
    @staticmethod
    def sim(*snds, mode='avg'):
        if mode == 'avg':
            def new_f(t):
                samples = [snd.f(t) for snd in snds if t <= snd.length]
                return sum(samples)/len(samples) if len(samples) > 0 else 0
        elif mode == 'add':
            def new_f(t):
                samples = [snd.f(t) for snd in snds if t <= snd.length]
                return sum(samples)
        return Sound(new_f, max([snd.length for snd in snds]))
    @staticmethod
    def from_pcm(data, srate, memoised = True):
        snd = Sound(id, len(data)/srate, memoised = memoised)
        snd._data = data
        def new_f(t):
            if len(snd._data) > t*srate:
                return snd._data[math.floor(t*srate)]
            else:
                return 0
        snd.f = new_f
        return snd
    @staticmethod
    def from_file(filename, memoised = True):
        nativesrate, data = wavfile.read(filename)
        widthinfo = np.iinfo(data.dtype)
        return Sound.from_pcm(data / min(widthinfo.max, abs(widthinfo.min)), nativesrate, memoised = memoised)


class Instrument:
    # a virtual instrument has a function that converts notes (note, length) to sounds
    # the note value is used as input for the scale function
    def __init__(self, f, scale, mode = 'avg'):
        self.f = f
        self.scale = scale
        self.mode = mode
    def play(self, notes):
        # notes is a list [(time, pitch, length), ...]
        # first, convert it into a list of (time, sound)
        notes = [(note[0], self.f(self.scale(note[1]), note[2])) for note in notes]
        def playnotes(t):
            a = 0
            relevant_notes = filter(lambda n: t >= n[0] and t <= n[0] + n[1].length, notes)
            # NB f(t - n[0]), we're counting time inside each note from 0, because they may include envelopes etc
            samples = [note[1].f(t - note[0]) for note in relevant_notes]
            if self.mode == 'avg':
                return sum(samples)/len(samples) if len(samples) > 0 else 0
            elif self.mode == 'add':
                return sum(samples)
            else:
                raise(Exception(f"unrecognised mode: {self.mode}"))
        return Sound(playnotes, max([n[0] + n[1].length for n in notes]))
