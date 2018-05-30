// Floors
// written by Eric heep

// Dog Star 2018
// ~-~-

public class Floors extends Chubgraph {
    CNoise p => LPF lpf => ADSR env => outlet;
    SinOsc s => blackhole;

    4::second => dur envDur;
    600 => float root;

    fun void init(float progress) {
        progress * 4.0::second + 4::second => envDur;
        (progress * -1.0) + 1.0 => float reverse;
        500 * progress + 400 => root;
        lpf.freq(root);
        s.freq(reverse * 5.0 + 2.0);
    }

    fun void keyOn() {
        env.attackTime(envDur);
        env.sustainLevel(1.0);
        env.keyOn();
        envDur => now;
    }

    fun void keyOff() {
        env.releaseTime(envDur);
        env.keyOff();
        envDur => now;
    }

    spork ~ modulate();

    fun void modulate() {
        while (true) {
            (s.last() + 1.0) * 0.5 => float scaled;
            lpf.freq(root + 40 * scaled);
            ms => now;
        }
    }

    p.gain(0.5);
}
