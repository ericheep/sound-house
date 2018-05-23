// Pads
// written by Eric heep

// Dog Star 2018
// ~-~-

public class Pads {
    CNoise p => LPF lpf => HPF hpf => Gain g => dac;
    SinOsc sin => blackhole;
    SinOsc mod => blackhole;

    400.0 => float root;

    // sin.sync(2);
    mod.freq(root/(4.0 * 1024.0));
    sin.freq(root);

    spork ~ modulate();

    fun void modulate() {
        while (true) {
            p.gain((mod.last() + 1.0) * 0.5 * 750 + 250);

            (mod.last() + 1.0) * 0.5 * 20.0 => float range;
            lpf.freq(root + range/2.0);
            hpf.freq(root - range/2.0);
            ms => now;
        }
    }
}

Pads p;
hour => now;
