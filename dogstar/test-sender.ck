OscOut out;

out.dest("192.168.0.7", 12345);

fun void ping() {
    while (true) {
        out.start("/w");
        out.send();
        100::ms => now;
    }
}

ping();
