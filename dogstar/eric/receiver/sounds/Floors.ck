// Floors
// written by Eric heep

// Dog Star 2018
// ~-~-

public class Floors extends Chubgraph {
    CNoise p => LPF lpf => ADSR env;
    SinOsc s;

    int running;

    fun void connect() {
        1 => running;
        s => blackhole;
        env => outlet;
    }

    fun void disconnect() {
        0 => running;
        s =< blackhole;
        env =< outlet;
    }

    fun void trigger(float progress) {
        connect();

        Math.pow(progress, 3) * 30.0::second + 15::second => dur envDur;
        (progress * -1.0) + 1.0 => float reverse;
        500 * progress + 400 => float root;
        spork ~ modulate(root);
        lpf.freq(root);
        s.freq(reverse * 5.0 + 2.0);

        env.set(envDur, 0::ms, 1.0, envDur);
        env.sustainLevel(1.0);
        env.keyOn();

        envDur => now;
        env.keyOff();
        envDur => now;

        disconnect();
    }

    fun int isRunning() {
        return running;
    }

    fun void modulate(float root) {
        while (running) {
            (s.last() + 1.0) * 0.5 => float scaled;
            lpf.freq(root + 40 * scaled);
            ms => now;
        }
    }

    p.gain(0.5);
}
