// NoiseTones
// written by Eric heep

// Dog Star 2018
// ~-~-

public class NoiseTones extends Chubgraph {
    CNoise p => LPF lpf => HPF hpf => Gain g => ADSR env => Gain master => outlet;
    Gain sinGain => master;

    SinOsc sin[4];
    SinOsc mod;

    int running;

    for (0 => int i; i < sin.size(); i++) {
        sin[i] => sinGain;
    }

    fun void trigger(float progress) {
        1 => running;
        mod => blackhole;
        env.attackTime(10::second);
        env.sustainLevel(1.0);
        env.keyOn();

        100.0 + 150.0 * progress => float root;

        for (0 => int i; i < sin.size(); i++) {
            sin[i].gain(0.60);
            sin[i].freq(root * Math.random2(1, 16));
        }

        mod.freq(0.2 + progress * 0.4);
        spork ~ modulate(root, progress);

        40::second => now;

        env.releaseTime(10::second);
        env.keyOff();
        10::second => now;
        mod =< blackhole;
        0 => running;
    }

    fun void modulate(float root, float progress) {
        while (running) {
            p.gain((mod.last() + 1.0) * 0.5 * 750 + 250 * progress);
            (mod.last() + 1.0) * 0.5 * 750 + 250 * progress

            (mod.last() + 1.0) * 0.5 * 20.0 => float range;
            lpf.freq(root + range/2.0);
            hpf.freq(root - range/2.0);

            sinGain.gain((mod.last() + 1.0) * 0.5 * -1.0 + 1.0);
            ms => now;
        }
    }
}

NoiseTones s => dac;
s.trigger(0.0);
