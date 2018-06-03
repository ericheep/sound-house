// NoiseTones
// written by Eric heep

// Dog Star 2018
// ~-~-

public class NoiseTones extends Chubgraph {
    CNoise p => LPF lpf => HPF hpf => Gain g => ADSR env => Gain master;
    Gain sinGain => env;

    SinOsc sin[4];
    SinOsc mod;

    for (0 => int i; i < sin.size(); i++) {
        sin[i] => sinGain;
    }

    int running;

    fun void connect() {
        master => outlet;
        mod => blackhole;
        1 => running;
    }

    fun void disconnect() {
        master =< outlet;
        mod =< blackhole;
        0 => running;
    }

    fun void trigger(float progress) {
        connect();

        (progress - 1.0) * -1.0 => float reverse;

        env.attackTime(10::second);
        env.sustainLevel(1.0);
        env.keyOn();

        100.0 + 100.0 * Math.pow(reverse, 3) => float root;

        for (0 => int i; i < sin.size(); i++) {
            sin[i].gain(0.40 * progress + 0.02);
            sin[i].freq(root * Math.random2(1, 16));
        }

        mod.freq(0.01 + Math.pow(reverse, 4) * 0.09);
        spork ~ modulate(root, reverse);
        35::second => now;

        env.releaseTime(10::second);
        env.keyOff();
        10::second => now;

        disconnect();
    }

    fun void modulate(float root, float progress) {
        while (running) {
            p.gain((mod.last() + 1.0) * 0.5 * 750 + 250 * progress);

            (mod.last() + 1.0) * 0.5 * 20.0 => float range;
            lpf.freq(root + range/2.0);
            hpf.freq(root - range/2.0);

            sinGain.gain((mod.last() + 1.0) * 0.5 * -1.0 + 1.0);
            ms => now;
        }
    }

    fun int isRunning() {
        return running;
    }
}
