// the sound you hear is the one you will be replacing
// sender script

// written by Cassia Streb
// ChucK realization by Eric Heep

// Dog Star 2018
// ~-~-

[
    "pione.local",
    "pitwo.local",
    "pithree.local",
    "pifour.local",
    "pifive.local",
    "pisix.local",
    "piseven.local",
    "pieight.local"
] @=> string IPS[];

[
    "pione",
    "pitwo",
    "pithree",
    "pifour",
    "pifive",
    "pisix",
    "piseven",
    "pieight"
] @=> string hostnames[];

float ultrasonicValues[hostnames.size()];

IPS.size() => int NUM_IPS;

// the port for outgoing messages
10001 => int OUT_PORT;
12345 => int ULTRASONIC_IN_PORT;
5000 => int ULTRASONIC_OUT_PORT;

OscOut ultrasonicOut[IPS.size()];
OscIn ultrasonicIn;
OscMsg ultrasonicMsg;

ULTRASONIC_IN_PORT => ultrasonicIn.port;
ultrasonicIn.listenAll();

OscOut out[NUM_IPS];
OscMsg msg;

for (0 => int i; i < NUM_IPS; i++) {
    out[i].dest(IPS[i], OUT_PORT);
    ultrasonicOut[i].dest(IPS[i], ULTRASONIC_OUT_PORT);
}


spork ~ ultrasonicListener();
spork ~ ultrasonicPing();

fun void ultrasonicListener() {
    while (true) {
        ultrasonicIn => now;
        while (ultrasonicIn.recv(msg)) {
            if (msg.address == "/w") {
                for (0 => int i; i < hostnames.size(); i++) {
                    if (msg.getString(0) == hostnames[i]) {
                        msg.getFloat(1) => float ultrasonicValue;
                        if (ultrasonicValue > 500.0) {
                            0.0 => ultrasonicValue;
                        }
                        Std.clampf(ultrasonicValue, 0.0, 300.0) => ultrasonicValue;
                        ultrasonicValue/300.0 => float gain;
                        <<< i, gain >>>;
                        setTargetMasterGain(i, gain);
                    }
                }
            }
        }
        1::samp => now;
    }
}

fun void ultrasonicPing() {
    while (true) {
        for (0 => int i; i < NUM_IPS; i++) {
            ultrasonicOut[i].start("/w");
            ultrasonicOut[i].send();
            50::ms => now;
        }
    }
}

// ~-~-

16.0::minute => dur pieceDuration;
1.0::minute => dur whiteNoiseDuration;
pieceDuration + whiteNoiseDuration => dur totalDuration;

15::second => dur minCellDuration;
2::minute => dur maxCellDuration;

[ 174.5,    // F3
  217.5,    // A3 (-14)
  349.0,    // F4
  479.875,  // B4 (-49)
  567.125,  // Db5 (+41)
  185.40625 // F#3 (+5)
] @=> float frequencies[];

2 => int maxSilences;
6 => int maxSineTones;
1 => int maxWhiteNoises;
2 => int maxPinkNoises;
2 => int maxTextures;
1 => int minTextures;

0 => int silenceCount;
0 => int sineToneCount;
0 => int whiteNoiseCount;
0 => int pinkNoiseCount;
0 => int textureCount;

int activeTextures[4];
for (0 => int i; i < activeTextures.size(); i++) {
    0 => activeTextures[i];
}

fun void cycleCell(int index, dur pieceDuration) {
    now => time beginning;

    while (now - beginning < pieceDuration) {
        playCell(index, pieceDuration);
    }
}

// ~-~-
// logic

fun void playCell(int index, dur duration) {
    Math.random2f(0.0, 1.0) * maxCellDuration + minCellDuration => dur duration;

    if (textureCount < minTextures) {
        playTexture(index, duration);
        return;
    }

    while (true) {
        Math.random2(0, 4) => int choice;

        if (choice == 0 && silenceCount < maxSilences) {
            playSilence(index, duration);
            return;
        } else if (choice == 1 && sineToneCount < maxSineTones) {
            playSineTone(index, duration);
            return;
        } else if (choice == 2 && whiteNoiseCount < maxWhiteNoises) {
            playWhiteNoise(index, duration);
            return;
        } else if (choice == 3 && pinkNoiseCount < maxPinkNoises) {
            playPinkNoise(index, duration);
            return;
        } else if (choice == 4 && textureCount < maxTextures) {
            playTexture(index, duration);
            return;
        }
    }
}

// osc senders
// ~-~-

fun void playSilence(int index, dur duration) {
    <<< index, "silence \t", duration/second >>>;
    silenceCount++;
    out[index].start("/silence");
    out[index].send();
    duration => now;
    silenceCount--;
}

fun void playSineTone(int index, dur duration) {
    <<< index, "sine tone \t", duration/second >>>;
    sineToneCount++;
    out[index].start("/sineTone");
    out[index].add(frequencies[Math.random2(0, frequencies.size() - 1)]);
    out[index].send();
    duration => now;
    sineToneCount--;
}

fun void playWhiteNoise(int index, dur duration) {
    <<< index, "white noise \t", duration/second >>>;
    whiteNoiseCount++;
    out[index].start("/whiteNoise");
    out[index].send();
    duration => now;
    whiteNoiseCount--;
}

fun void playPinkNoise(int index, dur duration) {
    <<< index, "pink noise \t", duration/second >>>;
    pinkNoiseCount++;
    out[index].start("/pinkNoise");
    out[index].send();
    duration => now;
    pinkNoiseCount--;
}

fun void playTexture(int index, dur duration) {
    <<< index, "texture \t", duration/second >>>;
    textureCount++;
    1 => int textureIsNotUnique;
    0 => int textureIndex;

    while (textureIsNotUnique) {
        Math.random2(0, 3) => textureIndex;
        if (activeTextures[textureIndex] == 0) {
            1 => activeTextures[textureIndex];
            0 => textureIsNotUnique;
        }
    }

    out[index].start("/texture");
    out[index].add(textureIndex);
    out[index].send();
    duration => now;
    0 => activeTextures[textureIndex];
    textureCount--;
}

fun void playWhiteNoiseFadeOut(int index, dur duration) {
    <<< index, "white noise fade out \t", duration/second >>>;
    out[index].start("/whiteNoiseFadeOut");
    out[index].add(duration/second);
    out[index].send();
    duration => now;
}

fun void setTargetMasterGain(int index, float gain) {
    out[index].start("/master");
    out[index].add(gain);
    out[index].send();
}

// main program
// ~-~-

fun void main() {
    for (0 => int i; i < IPS.size(); i++) {
        spork ~ cycleCell(i, pieceDuration);
    }

    5::second => now;
    setTargetMasterGain(0, 0.2);

    pieceDuration => now;

    for (0 => int i; i < IPS.size(); i++) {
        spork ~ playWhiteNoiseFadeOut(i, whiteNoiseDuration);
    }

    whiteNoiseDuration => now;
}

main();
