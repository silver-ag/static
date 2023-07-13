import math

# GENERATORS
# generators are functions of time in seconds to values between -1 and 1

# the adsr envelope is expected to be used for modulation rather than playing as a sound
# but any generators can be used for modulation if you want
def adsr(at, av, dt, dv, st, rt):
    #      av_
    #         /\
    #   dv_  /  \____
    #       /        \
    #      /          \_____
    #     at    dt  st rt
    def envelope(t):
        if t <= at:
            return av * t/at
        elif t <= dt:
            return (av * (1 - (t-at)/(dt-at))) + (dv * (t-at)/(dt-at))
        elif t <= st:
            return dv
        elif t <= rt:
            return dv * (1 - (t-st)/(rt-st))
        else:
            return 0
    return envelope

def silence():
    return lambda t: 0

# CLASSIC WAVES

def sinewave(freq, amp):
    if amp <= 1 and amp >= 0:
        return lambda t: amp*math.sin(t*2*math.pi*freq)
    else:
        raise(Exception('amplitude must be between 0 and 1'))

def sawtoothwave(freq,amp):
    if amp <= 1 and amp >= 0:
        return lambda t: ((t % (1/freq)) * freq * amp * 2) - amp
    else:
        raise(Exception('amplitude must be between 0 and 1'))

def trianglewave(freq,amp):
    if amp <= 1 and amp >= 0:
        return lambda t: (abs((t % (1/freq))*freq - 0.5) * 4 * amp) - amp
    else:
        raise(Exception('amplitude must be between 0 and 1'))

def squarewave(freq,width,amp):
    if amp > 1 or amp < 0:
        raise(Exception('amplitude must be between 0 and 1'))
    elif width > 1 or width < 0:
        raise(Exception('width must be between 0 and 1'))
    else:
        return lambda t: amp if (t % (1/freq))*freq < width else -amp
