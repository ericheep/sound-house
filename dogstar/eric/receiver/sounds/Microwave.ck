// Microwave
// written by Eric heep

// Dog Star 2018
// ~-~-

public class Microwave extends Chubgraph {
    CNoise p => TriOsc tri => HPF hpf => LPF lpf => ADSR env;
    SinOsc s;

    int running;

    fun void connect() {
        env => outlet;
        s => blackhole;
        1 => running;
    }

    fun void disconnect() {
        env =< outlet;
        s =< blackhole;
        0 => running;
    }

    spork ~ modulate();

    fun void modulate() {
        while (true) {
            tri.gain((s.last() + 1.0) * 0.5 * 0.2 + 0.8);
            ms => now;
        }
    }

    fun void trigger(float progress) {
        connect();

        (progress - 1.0) * -1.0 => float reverse;

        spork ~ falling();

        s.freq(8);
        hpf.freq(1800);
        lpf.freq(1100);
        tri.sync(2);
        tri.freq(1500 * reverse + 500);
        env.set(20::ms, 0::ms, 1.0, 20::ms);

        0.1::second + reverse * 0.3::second => dur duration;

        repeat(2) {
            env.keyOn();
            duration => now;
            env.keyOff();
            duration => now;
        }

        disconnect();
    }

    fun void falling() {
        while (running) {
            tri.freq(tri.freq() - 0.02);
            env.gain(env.gain() - 0.0002);
            ms => now;
        }
    }

    fun int isRunning() {
        return running;
    }
}

Microwave m => dac;
m.trigger(1.0);
