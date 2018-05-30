// Wichita
// written by Eric heep

// Dog Star 2018
// ~-~-

public class Wichita extends Chubgraph {
    SndBuf w => LPF lpf => ADSR env => outlet;
    lpf.freq(2000);
    w.gain(0.5);

    fun void fallingRate(float initialRate) {
        float inc;
        while (initialRate - inc > 0) {
            -0.00005 -=> inc;
            w.rate(initialRate - inc);
            5::ms => now;
        }
    }

    fun void trigger(float progress) {
        w.read("wichita-line.wav");
        progress * 0.4 + 0.6 => float initialRate;
        w.rate(initialRate);

        spork ~ fallingRate(initialRate);

        w.pos(0);
        env.attackTime(20::ms);
        env.sustainLevel(1.0);
        env.keyOn();
        20::ms => now;

        env.releaseTime(7::second);
        env.keyOff();
        7::second => now;
    }
}
