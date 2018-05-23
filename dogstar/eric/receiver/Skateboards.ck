// Skateboards
// written by Eric heep

// Dog Star 2018
// ~-~-

public class Skateboards {
    CNoise p => LPF lpf => HPF hpf => Gain g => dac;

    SinOsc sin[2];
    Gain sinGain => dac;
    SinOsc mod => blackhole;

    Math.random2f(100.0, 250.0) => float root;

    for (0 => int i; i < sin.size(); i++) {
        sin[i].gain(0.05);
        sin[i] => sinGain;
        sin[i].freq(root * Math.random2(1, 16));
    }

    mod.freq(Math.random2f(0.02, 0.06));
    spork ~ modulate();

    fun void modulate() {
        while (true) {
            p.gain((mod.last() + 1.0) * 0.5 * 750 + 250);

            (mod.last() + 1.0) * 0.5 * 20.0 => float range;
            lpf.freq(root + range/2.0);
            hpf.freq(root - range/2.0);

            sinGain.gain((mod.last() + 1.0) * 0.5 * -1.0 + 1.0);
            ms => now;
        }
    }
}

Skateboards s;
hour => now;
