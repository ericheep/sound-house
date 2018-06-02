// Freezer
// written by Eric heep

// Dog Star 2018
// ~-~-

public class Freezer extends Chubgraph {

    class Distortion extends Chugen {
        fun float tick(float in) {
            Math.pow(in, 0.95) => in;

            while (in > 1.0 || in < -1.0) {
                if (in > 1.0) {
                    1.0 - (in - 1.0) => in;
                }
                if (in < -1.0) {
                    -1.0 - (in + 1.0) => in;
                }
            }
            return in;
        }
    }

    SinOsc mod => SinOsc sin => ADSR env => LPF lpf => HPF hpf => outlet;
    sin.sync(2);

    TriOsc sin2 => env;
    SinOsc am;
    SinOsc ring;

    int running;

    fun void connect() {
        hpf => outlet;
        am => blackhole;
        ring => blackhole;
        1 => running;
    }

    fun void disconnect() {
        hpf =< outlet;
        am =< blackhole;
        ring =< blackhole;
        0 => running;
    }

    fun void trigger(float progress) {
        connect();

        spork ~ modulate();
        (progress - 1.0) * -1.0 => float reverse;

        Math.pow(reverse, 3) * 40 + 62 => float root;

        ring.freq(40 * reverse + 10);
        sin.freq(root);
        sin2.freq(root * 2.5);
        lpf.freq(root * 6);
        hpf.freq(root + root * 2 * reverse);
        lpf.Q(0.5);
        hpf.Q(0.75);
        hpf.gain(1.0);

        spork ~ slide(root);

        am.freq(1.2 - 1.0 * progress);

        sin.gain(Math.pow(reverse, 4) * 0.2 + 0.8);

        mod.freq(root * 8.0);
        mod.gain(150);
        sin.sync(2);

        env.set(5::second, 0::ms, 1.0, 5::second);
        env.keyOn();
        35::second => now;

        env.keyOff();
        5::second => now;
        disconnect();
    }

    fun void slide(float freq) {
        while (running) {
            sin.freq(freq + am.last() * 2.0);
            lpf.gain((ring.last() + 1.0) * 0.5);
            ms => now;
        }
    }

    fun void modulate() {
        while (running) {
            sin.gain(Math.pow((am.last() + 1.0) * 0.5 * 0.8, 3) + 0.2);
            sin2.gain((((am.last() + 1.0) * 0.5 * - 1.0 * -1.0) * 0.2) + 0.4);
            ms => now;
        }
    }

    fun int isRunning() {
        return running;
    }
}

Freezer f => dac;
f.gain(0.1);
f.trigger(1.0);
