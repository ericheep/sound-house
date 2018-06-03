// Traffic
// written by Eric heep

// Dog Star 2018
// ~-~-

public class Traffic extends Chubgraph {
    CNoise p => LPF lpf => HPF hpf => Gain g => ADSR env;
    SinOsc mod => blackhole;

    int running;

    fun void connect() {
        env => outlet;
        1 => running;
    }

    fun void disconnect() {
        env =< outlet;
        0 => running;
    }

    fun void trigger(float progress) {
        connect();
        1030.0 * progress + 1000.0 => float root;

        (progress - 1.0) * -1.0 => float reverse;
        // g.gain(0.6 + 0.4 * reverse);

        spork ~ falling(root);
        spork ~ modulate(root * reverse + 35.0);

        env.set(10::second, 0::ms, 1.0, 10::second);
        env.keyOn();
        10::second => now;

        progress * 10::second => now;
        env.keyOff();
        10::second => now;
        disconnect();
    }

    fun void falling(float root) {
        while (running) {
            if (root > 30) {
                0.01 -=> root;
            }
            mod.freq(root/(4.0 * 1024.0));
            ms => now;
        }
    }

    fun void modulate(float root) {
        while (running) {
            p.gain((mod.last() + 1.0) * 0.5);

            (mod.last() + 1.0) * 0.5 * 20.0 => float range;
            lpf.freq(root + range/2.0);
            hpf.freq(root - range/2.0);
            ms => now;
        }
    }

    fun int isRunning() {
        return running;
    }
}
