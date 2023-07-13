from .classes import Instrument, Sound
from .generators import adsr, sinewave, trianglewave
from .effects import amp_mod, pitch_shift
from .scales import classical_scale

class SineInstrument(Instrument):
    def __init__(self, amplitude = 0.7, scale = classical_scale):
        super().__init__(self.f, scale, mode = 'avg')
        self.amplitude = amplitude
    def f(self, pitch, length):
        return Sound(amp_mod(sinewave(pitch, self.amplitude), adsr(0.3*length, 1, 0.6*length, 0.5, 0.8*length, length)), length)

class TriangleInstrument(Instrument):
    def __init__(self, amplitude = 0.7, scale = classical_scale):
        super().__init__(self.f, scale, mode = 'avg')
        self.amplitude = amplitude
    def f(self, pitch, length):
        return Sound(amp_mod(trianglewave(pitch, self.amplitude), adsr(0.3*length, 1, 0.6*length, 0.5, 0.8*length, length)), length)

class SampleInstrument(Instrument):
    # assumes the sample is at A440 by default
    def __init__(self, sample, samplepitch = 440, scale = classical_scale):
        super().__init__(self.f, scale, mode = 'avg')
        self.sample = sample
        self.basepitch = samplepitch
    def f(self, pitch, length):
        return Sound(pitch_shift(self.sample.f, pitch/self.basepitch), min(self.sample.length, length))

class SampleBoard(Instrument):
    # just provide a list or dict of Sounds and acess them through an instrument
    # eg. as a drumkit
    def __init__(self, samples):
        super().__init__(self.f, lambda x: x, mode = 'avg')
        self.samples = samples
    def f(self, pitch, length):
        s = self.samples[pitch]
        s.length = length
        return s
