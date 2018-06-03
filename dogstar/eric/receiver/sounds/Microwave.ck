// Microwave
// written by Eric heep

// Dog Star 2018
// ~-~-

public class Microwave {
    CNoise p => TriOsc tri => HPF hpf => LPF lpf => ADSR env => dac;
    SinOsc s => blackhole;
    s.freq(8);

    hpf.freq(1800);
    lpf.freq(1100);
    tri.sync(2);
    tri.freq(2000);

    spork ~ modulate();

    fun void modulate() {
        while (true) {
            tri.gain((s.last() + 1.0) * 0.5 * 0.2 + 0.8);
            ms => now;
        }
    }

    repeat(2) {
        env.keyOn();
        1.4::second => now;
        env.keyOff();
        1.4::second => now;
    }
}

Microwave s;
hour => now;
