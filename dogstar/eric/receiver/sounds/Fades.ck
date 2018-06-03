// Fades
// written by Eric heep

// Dog Star 2018
// ~-~-

public class Fades extends Chubgraph {
    CNoise p => TriOsc t => Dyno d => LPF lpf => ADSR win => ADSR env;
    SinOsc s => t;

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

        p.gain(150);
        s.gain(15000);
        t.sync(2);

        (progress - 1.0) * -1.0 => float reverse;
        450.0 + 2150.0 * progress => float freq;

        s.freq(freq * 0.5);
        t.freq(freq);
        lpf.freq(freq/2.0);

        env.gain(1.0 - progress * 0.95);

        spork ~ windowModulate(reverse);

        float envelope[10];
        for (0 => int i; i < envelope.size(); i++) {
            Math.random2f(1.0, 2.0 * progress + 2.0) => envelope[i];
        }

        envelopePath(envelope);

        disconnect();
    }

    fun dur drunkMovement(dur drunk, dur min, dur max, float progress) {
        Math.random2f(0.2, 0.3 + 0.7 * progress)::ms => dur distance;
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

    fun void windowModulate(float progress) {
        10::ms => dur min;
        20::ms => dur max;
        Math.random2f(0.0, 1.0) * max + min => dur attackSpace;
        Math.random2f(0.0, 1.0) * max + min => dur releaseSpace;

        while (true) {
            attackSpace;
            win.attackTime(5::ms);
            win.keyOn();
            attackSpace => now;
            win.keyOff();
            win.releaseTime(5::ms);
            releaseSpace => now;

            drunkMovement(attackSpace, min, max, progress) => attackSpace;
            drunkMovement(releaseSpace, min, max, progress) => releaseSpace;
        }
    }

    fun void envelopePath(float seconds[]) {
        seconds.size() => int N;
        for (0 => int i; i < N; i++) {
            seconds[i]::second => dur duration;
            if (i % 2 == 0) {
                env.attackTime(duration);
                env.keyOn();
            } else {
                env.releaseTime(duration + Math.random2f(0.5, 1.0) * duration);
                env.keyOff();
            }
            duration => now;
        }

        seconds[seconds.size() - 1]::second => now;
    }

    fun int isRunning() {
        return running;
    }
}
