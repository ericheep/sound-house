// Freezer
// written by Eric heep

// Dog Star 2018
// ~-~-

public class Freezer extends Chubgraph {

    class Distortion extends Chugen {
        fun float tick(float in) {
            2.5 *=> in;
            while (in > 1.0 && in < -1.0) {
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

    SinOsc mod => SinOsc sin => ADSR env => LPF lpf => Distortion dist => HPF hpf => outlet;

    SinOsc sin2 => env;
    sin.sync(2);

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
        (progress - 1.0) * -1.0 => progress;

        spork ~ modulate();

        Math.pow(progress, 3) * 40 + 62 => float root;

        ring.freq(40 * progress + 10);
        sin.freq(root);
        sin2.freq(root * 3);
        lpf.freq(2200);
        hpf.freq(root + root * 3 * progress);
        lpf.Q(0.5);
        hpf.Q(0.75);
        hpf.gain(0.2 + progress * 0.8);

        spork ~ slide(root);

        am.freq(0.4 + 1.6 * progress);

        (progress - 1.0) * -1.0 => float reverse;
        sin.gain(Math.pow(progress, 4) * 0.6 + 0.4);

        mod.freq(root * 16.0);
        mod.gain(150);
        sin.sync(2);

        env.set(5::second, 0::ms, 1.0, 5::second);
        env.keyOn();
        25::second => now;

        env.keyOff();
        5::second => now;
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
            sin2.gain((((am.last() + 1.0) * 0.5 * - 1.0 * -1.0) * 0.2) + 0.2);
            ms => now;
        }
    }

    fun int isRunning() {
        return running;
    }
}
