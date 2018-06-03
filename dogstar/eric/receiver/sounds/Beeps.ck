// Beeps
// written by Eric heep

// Dog Star 2018
// ~-~-

public class Beeps extends Chubgraph {
    CNoise p => TriOsc t => Dyno d => LPF lpf => ADSR env;
    SinOsc s;

    int running;

    fun void connect() {
        s => blackhole;
        env => outlet;
        1 => running;
    }

    fun void disconnect() {
        s =< blackhole;
        env =< outlet;
        0 => running;
    }

    fun void trigger(float progress) {
        connect();

        spork ~ falling();
        spork ~ modulate();

        (progress - 1.0) * -1.0 => float reverse;
        <<< reverse >>>;
        s.freq(2850 * reverse);
        t.sync(2);
        lpf.freq(700);
        env.set(40::ms, 0::ms, 1.0, 40::ms);
        env.keyOn();
        t.freq(860.0 * reverse + 400);
        100::ms * 0.5 => now;
        env.keyOff();
        100::ms * 0.5 => now;

        env.keyOn();
        100::ms - 40::ms => now;
        env.keyOff();
        100::ms => now;

        disconnect();
    }


    fun void falling() {
        while (running) {
            t.freq(t.freq() - 0.25);
            t.gain(t.gain() - 0.0002);
            ms => now;
        }
    }

    fun void modulate() {
        while (running) {
            p.gain((s.last() + 1.0) * 0.5 * 30);
            ms => now;
        }
    }

    fun int isRunning() {
        return running;
    }
}
