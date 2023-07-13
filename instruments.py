from .classes import Instrument, Sound
from .generators import adsr, sinewave
from .effects import amp_mod, pitch_shift
from .scales import classical_scale

class SineInstrument(Instrument):
    def __init__(self, amplitude = 0.7):
        super().__init__(self.f, TET, mode = 'avg')
        self.amplitude = amplitude
    def f(self, pitch, length):
        return Sound(amp_mod(sinewave(pitch, self.amplitude), adsr(0.3*length, 1, 0.6*length, 0.5, 0.8*length, length)), length)

class SampleInstrument(Instrument):
    # assumes the sample is at A440 by default
    def __init__(self, sample, samplepitch = 440):
        super().__init__(self.f, mode = 'avg')
        self.sample = sample
        self.basepitch = samplepitch
    def f(self, pitch, length):
        return Sound(pitch_shift(self.sample.f, pitch/self.basepitch), min(self.sample.length, length))
