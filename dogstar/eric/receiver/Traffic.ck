// Traffic
// written by Eric heep

// Dog Star 2018
// ~-~-

public class Traffic {
    CNoise p => LPF lpf => HPF hpf => Gain g => dac;
    SinOsc mod => blackhole;

    2030.0 => float root;

    spork ~ modulate();
    spork ~ falling();

    fun void falling() {
        while (true) {
            if (root > 20) {
                0.01 -=> root;
                <<< root >>>;
            }
            mod.freq(root/(4.0 * 1024.0));
            ms => now;
        }
    }

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

Traffic t;
hour => now;
