# kinet.py

<img src="http://i.imgur.com/StIq4To.jpg" />

This is a simple object oriented python interface for Color Kinetics "kinet"
protocol, written by Giles Hall.  It is used to drive color kinetics lights
over ethernet.  It is pretty easy to get started with.

## PowerSupply

A PowerSupply class is an encapsulation of a network attached Color Kinetics
power supply, such as the PDS-150e.  The PowerSupply class handles building a
Header object, which initiates all communications with Color Kinetics network
attached devices.  If you need to customize the Header payload, this is easily
done by making a Header object, changing the attribute in question, and using
it as a argument for the PowerSupply's constructor.  The default Header should
work in most circumstances.  If your power supply's IP address was
"192.168.1.120", you would simply say the following to instantiate a
PowerSupply object: 

<pre>
>>> pds = PowerSupply("192.168.1.120")
</pre>

## Fixture

A fixture is an encapsulation of a single, addressable light fixture.
Currently, there is only one Fixture type supported, and that is an RGB
fixture.  You could extend the Fixture class for RGBAW and white only fixture
types. 

The RGB fixture allows you to easily control its RGB values through attributes.
You can also get or set the RGB values using HSV, which are internally
converted.  This makes it easy to write rainbow cycles.  See example.py for an
example on how to do this.

Fixtures are constructed on their lowest DMX address value.  For example, if a
RGB fixture spans (3,4,5), you would build the fixture object on 3 like so: 

```
>>> fix = FixtureRGB(3)
```

The PowerSupply class inherits from list.  To bind a fixture to a PowerSupply,
all you need to do is append it:

```
>>> pds = PowerSupply("192.168.1.120")
>>> fix = FixtureRGB(3)
>>> pds.append(fix)
```

To change a value on the lights, you would simply tell the PowerSupply to go():

```
>>> pds = PowerSupply("192.168.1.120")
>>> fix = FixtureRGB(3)
>>> pds.append(fix)
>>> pds[0].rgb = (255, 0, 0)
>>> pds.go()
```

## FadeIter

FadeIter is a convenience class to allow smooth transitions between two
different scenes.  It will fade all the 512 channels between two different
scenes for a duration of time.  For example, if we wanted to fade the first
fixture from all off to entirely on over a ten second period, we would simply
write the following:

```
>>> pds1 = PowerSupply("192.168.1.120")
>>> pds1.append(fix)
>>> pds2 = pds1.copy()
>>> pds2[0].rgb = (255, 255, 255)
>>> fi = FadeIter(pds1, pds2, 10)
>>> fi.go()
```

## Examples of kinet.py in the Wild

A group of students from Drexel used kinet.py to drive a
[http://arstechnica.com/gaming/2013/04/selling-coding-and-playing-the-worlds-largest-videogame/ 30-story version of Pong in Philadelphia].

[https://github.com/Dewb Michael Dewberry] ported kinet.py to
C++ to drive a ColorKinetics video wall of LEDs.  You can find it within his
[https://github.com/Dewb/alphadep alphadep] project.

## Dedication

This library is dedicated to the memory of Kevin "Frostbyte" McCormick, a
brilliant light artist who continues to be a source of inspiriation for the
EE/LED community at large.