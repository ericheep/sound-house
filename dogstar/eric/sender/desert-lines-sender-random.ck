// desert lines random test
// sender script

// written by Eric Heep
// Dog Star 2018
// ~-~-

// order ~-~-

// floor        1:00 - 3:30
// bumps        2:00 - 4:00
// fades        3:30 - 5:00
// noiseTones   3:00 - 5:30
// gasStation   5:00 - 7:00
// freezer      5:30 - 8:15
// wichita      7:00 - 7:30

[
    "ethel.local", "vera.local"
] @=> string hostnames[];

PiHandler ph;
ph.init(hostnames, 10001);

dur floorStart;
dur floorEnd;
dur noiseStart;
dur noiseEnd;
dur gasStationStart;
dur gasStationEnd;
dur wichitaStart;
dur wichitaEnd;

while (true) {
    ph.send(0, "/wichita", Math.random2f(0.0, 1.0));
    3::second => now;
    ph.send(1, "/wichita", Math.random2f(0.0, 1.0));
    6::second => now;
}

