// Subway
// written by Eric heep

// Dog Star 2018
// ~-~-

public class Subway {
    SinOsc mod => TriOsc tri => HPF hpf => LPF lpf => ADSR env => dac;
    SinOsc s => blackhole;
    s.freq(800);

    620.0 * 2 => float root;

    hpf.freq(1800);
    lpf.freq(1100);
    tri.sync(2);
    tri.freq(root);

    mod.freq(root * 2.0 + 2.0);
    mod.gain(100);

    spork ~ modulate();

    fun void modulate() {
        while (true) {
            tri.gain((s.last() + 1.0) * 0.5 * 0.3 + 0.7);
            ms => now;
        }
    }

    200::ms => dur release;
    10::ms => dur attack;
    env.set(10::ms, 0::ms, 1.0, 200::ms);
    repeat(2) {
        tri.freq(root);
        env.keyOn();
        attack => now;
        env.keyOff();
        release => now;
        tri.freq(root * 4.0/5.0);
        env.keyOn();
        attack => now;
        env.keyOff();
        release - 70::ms => now;
    }
    second => now;
}

Subway s;
hour => now;
