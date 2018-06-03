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

fun void addSound(string addr, dur start, dur end) {
    Sound sound;
    sound.set(addr, start, end);
    sounds << sound;
}

addSound("/floor",       1.00::minute, 4.00::minute);
addSound("/bumps",       3.00::minute, 6.00::minute);
addSound("/noiseTones",  2.50::minute, 6.50::minute);
addSound("/fades",       5.75::minute, 8.50::minute);
addSound("/beeps",       6.50::minute, 8.00::minute);
addSound("/gasStation",  8.50::minute, 10.00::minute);
addSound("/freezer",     7.50::minute, 11.50::minute);
addSound("/stoned",      7.75::minute, 8.75::minute);
addSound("/microwave",   9.00::minute, 10.50::minute);
addSound("/wichita",     9.50::minute, 11.50::minute);
addSound("/traffic",     11.25::minute, 14.00::minute);
addSound("/end",         14.00::minute, 20.00::minute);

UltrasonicHandler uh;
uh.setEmulation();
uh.init(hostnames, 5000, 12345);

PiHandler ph;
ph.init(hostnames, 10001);

while (true) {
    uh.passingEvent => now;
    uh.passingEvent.value => int index;
    for (0 => int i; i < sounds.size(); i++) {
        sounds[i].getProgress(now) => float progress;
        if (progress >= 0.0) {
            ph.send(index, sounds[i].getAddress(), progress);
        }
    }
}
