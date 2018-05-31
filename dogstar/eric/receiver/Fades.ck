// Fades
// written by Eric heep

// Dog Star 2018
// ~-~-

public class Fades {
    CNoise p => TriOsc t => Dyno d => LPF lpf => WinFuncEnv win => PowerADSR env => dac;
    SinOsc s => t;

    fun void test() {
        p.gain(50);
        s.gain(15000);
        t.sync(2);

        Math.random2f(950.0, 1150.0) => float freq;

        s.freq(freq * 2);
        t.freq(freq);
        lpf.freq(freq/2.0);

        spork ~ windowModulate();

        float envelope[10];
        for (0 => int i; i < envelope.size(); i++) {
            Math.random2f(1.5, 3.0) => envelope[i];
        }

        envelopePath(envelope);
    }

    fun dur drunkMovement(dur drunk, dur min, dur max) {
        Math.random2f(0.2, 0.3)::ms => dur distance;
        if (drunk < min) {
            distance +=> drunk;
        } else if (drunk > max) {
            distance -=> drunk;
        } else {
            if (maybe) {
                distance +=> drunk;
            } else {
                distance -=> drunk;
            }
        }

        return drunk;
    }

    fun void windowModulate() {
        10::ms => dur min;
        20::ms => dur max;
        Math.random2f(0.0, 1.0) * max + min => dur attackSpace;
        Math.random2f(0.0, 1.0) * max + min => dur releaseSpace;

        while (true) {
            attackSpace;
            win.setParzen();
            win.keyOn();
            win.attackTime(5::ms);
            attackSpace => now;
            win.keyOff();
            win.releaseTime(5::ms);
            releaseSpace => now;

            drunkMovement(attackSpace, min, max) => attackSpace;
            drunkMovement(releaseSpace, min, max) => releaseSpace;
            <<< attackSpace/ms, releaseSpace/ms >>>;
        }
    }

    fun void envelopePath(float seconds[]) {
        seconds.size() => int N;
        for (0 => int i; i < N; i++) {
            seconds[i]::second => dur duration;
            if (i % 2 == 0) {
                env.attackCurve(Math.random2f(1.5, 2.5));
                env.attack(duration);
                env.keyOn();
            } else {
                env.releaseCurve(Math.random2f(0.25, 0.75));
                env.release(duration + Math.random2f(0.1, 0.25) * duration);
                env.keyOff();
            }
            duration => now;
        }

        seconds[seconds.size() - 1]::second => now;
    }
}

Fades f;
f.test();
