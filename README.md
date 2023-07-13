# Static - a music-making library

**Static** provides tools for making music. Basic usage:
```python
from static import StaticPlayer, Sound
from static.generators import sinewave

p = StaticPlayer()
s = Sound(sinewave(440, 1), 1) # a one-second A440

p.play(s)
```

### Examples

make a little tune:
```python
from static import StaticPlayer, Sound
from static.instruments import SineInstrument

p = StaticPlayer()
piano = SineInstrument()

# each note being passed to <instrument>.play is in the form (<start time>, <note>, <duration>)
# all times are in seconds
track = piano.play([(0,'A4',1), (1, 'C4', 1), (2, 'E4', 1), (3, 'A4', 1), (3, 'C4', 1), (3, 'E4', 1)])

p.save(track, '/tmp/output.wav')
```

make your voice deeper:
```python
from static import StaticPlayer, Sound
from static.effects import pitch_shift

voice = Sound.from_file('speaking.wav')
# sounds are represented by a function of time to amplitude
# the underlying function of a sound is accessible at <sound>.f
deep_voice = Sound(pitch_shift(voice.f, 0.75), voice.length)

p.play(deep_voice)
```
