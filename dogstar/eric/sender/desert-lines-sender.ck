// desert lines
// sender script

// written by Eric Heep
// Dog Star 2018
// ~-~-

// order ~-~-

// floor        1:00 - 3:00
// bumps        2:30 - 5:00
// noiseTones   3:00 - 5:30
// gasStation   5:00 - 7:00
// freezer      5:30 - 8:45
// wichita      7:00 - 8:00
// stoned       7:45 - 8:45
// sun          8:15 - 9:15
// traffic      9:00 - 13:00

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

// addSound("/floor", 1.5::minute, 4.5::minute);
// addSound("/bumps", 2.5::minute, 6.5::minute);
// addSound("/noiseTones", 4.0::minute, 8.0::minute);
// addSound("/gasStation", 7.0::minute, 8.0::minute);
// addSound("/wichita1", 0.0::minute, 0.4::minute);
// addSound("/stone1", 0.0::minute, 0.4::minute);

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
