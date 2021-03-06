// Chimes
// written by Eric heep

// Dog Star 2018
// ~-~-

public class Beeps extends Chubgraph {
    CNoise p => TriOsc t => Dyno d => LPF lpf => ADSR env => outlet;
    SinOsc s;

    int running;

    fun void playBeeps() {
        s.freq(2850);
        t.sync(2);
        lpf.freq(700);
        env.set(40::ms, 0::ms, 1.0, 40::ms);
        env.keyOn();
        t.freq(1260.0);
        100::ms * 0.5 => now;
        env.keyOff();
        100::ms * 0.5 => now;

        env.keyOn();
        100::ms - 40::ms => now;
        env.keyOff();
        40::ms => now;
    }

    fun void playMaj6() {
        s.freq(105);
        t.sync(2);
        lpf.freq(500);
        env.set(40::ms, 0::ms, 1.0, 30::ms);

        352.0 => float root;
        5.0/3.0 => float ratio;

        env.keyOn();
        t.freq(root);
        0.15::second => now;
        t.freq(root * ratio);
        0.325::second  - 30::ms => now;
        env.keyOff();
        30::ms => now;
    }

    fun void falling() {
        while (running) {
            t.freq(t.freq() - 0.02);
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
}

Chimes c => dac;
c.gasStation(1.0);
// c.playMaj3();
//c.playBeeps();
