import math
import re

def nthroot(x, n):
    return math.exp(math.log(x)/n)

def make_ET(steps, base = 440):
    def scale(n):
        return base * math.pow(nthroot(2, steps), n)
    return scale

def classical_scale(note):
    internal_scale = make_ET(12, 440)
    if isinstance(note, int):
        return internal_scale(note)
    elif isinstance(note, str):
        breakdown = re.match('([a-gA-G])([b#]?)([0-9]+)', note)
        if breakdown:
            letter = breakdown.group(1)
            accidental = breakdown.group(2)
            octave = breakdown.group(3)
            notevalue = {'a': 0, 'b': 2, 'c': 3, 'd': 5, 'e': 7, 'f':8, 'g': 10}[letter]
            accidentalvalue = {'#': 1, 'b': -1, '': 0}[accidental]
            octavevalue = int(octave)
            return internal_scale(((octavevalue - 4) * 12) + notevalue + accidentalvalue)
        else:
            raise(Exception(f'invalid note representation: "{note}"'))
            
