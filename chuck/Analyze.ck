// Analyze.ck
// simple envelope following

public class Analyze extends Chubgraph {

    inlet => Gain g => OnePole p => blackhole;
    inlet => g;

    // rms stuff
    3 => g.op;
    0.9999 => p.pole;

    fun void setPole(float pole) {
        pole => p.pole;
    }

    fun float decibel() {
        return Std.rmstodb(p.last());
    }

    // merely holds until a spike is heard above a certain level
    fun void decibelOver(float db) {
        while (decibel() < db) {
            1::samp => now;
        }
    }

    fun void decibelUnder(float db) {
        while (decibel() > db) {
            1::samp => now;
        }
    }
}

/*
Analyze a;

adc.chan(0) => a;

a.setPole(0.99);

while (true) {
    <<< a.decibel() >>>;
    10::ms => now;
}
*/
