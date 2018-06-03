// desert lines
// sender script

// written by Eric Heep
// Dog Star 2018
// ~-~-

// order ~-~-

// floor        1:00 - 4:00
// bumps        2:30 - 5:15
// noiseTones   3:00 - 6:30
// fades        5:00 - 8:00
// gasStation   7:30 - 8:15
// beeps        6:00 - 7:00
// freezer      6:30 - 10:15
// stoned       7:45 - 8:45
// microwave    8:30 - 9:30
// wichita      9:30 - 10:30
// traffic      10:00 - 13:00

/* [ */
/*     "pione.local", "pitwo.local", "pithree.local", "pifour.local", */
/*     "pifive.local", "pisix.local", "piseven.local", "pieight.local" */
/* ] @=> string hostnames[]; */

[ "ethel.local", "vera.local" ] @=> string hostnames[];

Sound sounds[0];

fun void addSound(string addr, dur start, dur end, float gain) {
    Sound sound;
    sound.set(addr, start, end, gain);
    sounds << sound;
}

// score ~

// section one
addSound("/floor",       1.00::minute,  5.00::minute,   1.00);

// section two
addSound("/noiseTones",  4.50::minute,  8.50::minute,   0.20);
addSound("/bumps",       5.00::minute,  8.00::minute,   1.00);
addSound("/fades",       7.75::minute,  12.00::minute,  0.75);
addSound("/beeps",       9.50::minute,  11.25::minute,  0.45);

// section three
addSound("/freezer",     11.75::minute, 16.00::minute,  0.15);
addSound("/gasStation",  12.25::minute, 13.50::minute,  0.30);
addSound("/wichita2",    12.50::minute, 13.50::minute,  0.20);
addSound("/stone2",      13.00::minute, 14.50::minute,  0.30);
addSound("/microwave",   13.50::minute, 14.50::minute,  0.004);
addSound("/stone1",      14.00::minute, 15.15::minute,  0.30);
addSound("/wichita1",    14.50::minute, 15.50::minute,  0.20);

// section four
addSound("/floor",       15.75::minute, 17.50::minute,  1.00);
addSound("/traffic",     14.75::minute, 16.75::minute,  1.00);
addSound("/end",         17.50::minute, 20.00::minute,  0.00);

UltrasonicHandler uh;
uh.setEmulation();
uh.init(hostnames, 5000, 12345);

PiHandler ph;
ph.init(hostnames, 10001);

while (true) {
    uh.passingEvent => now;
    uh.passingEvent.value => int index;
    for (0 => int i; i < sounds.size(); i++) {
        sounds[i].getProgress(now + 14.00::minute) => float progress;
        sounds[i].getGain() => float gain;
        if (progress >= 0.0) {
            ph.send(index, sounds[i].getAddress(), progress, gain);
        }
    }
}
