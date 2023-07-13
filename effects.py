import math

# EFFECTS
# effects take generator functions to new functions

def amp_mod(f, env):
    return lambda t: f(t) * env(t)

def amplify(f, multiplier):
    return lambda t: f(t) * multiplier

def pitch_shift(f, multiplier, chunk = 0.1):
    # very low quality pitch shift algorithm with lots of wobbly artifacts :D
    # average of two half-chunk offset tracks
    # in each, simply play faster or slower by <multiplier> but every <chunk> skip to remain in time with the original
    # note that the chunk must be larger than the wavelength, ideally by a decent amount, but smaller than any larger features. 0.1s is the default
    def roundoffset(num, chunk, offset):
        # take values of the form offset + n*chunk + (x < chunk) and return the corresponding offset + n*chunk
        # so for chunk = 0.1, offset = 0.05, it'll take eg (0.25, 0.349) to 0.25
        nchunks = math.floor((num - offset) / chunk)
        return (nchunks * chunk) + offset
    def new_f(t):
        a = roundoffset(t, chunk, 0)
        b = roundoffset(t, chunk, chunk/2)
        return (f(a + (multiplier * (t - a))) + f(b + (multiplier * (t - b)))) / 2
    return new_f
