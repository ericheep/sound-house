// the sound you hear is the one you will be replacing
// sender script

// written by Cassia Streb
// ChucK realization by Eric Heep

// Dog Star 2018
// ~-~-

UltrasonicHandler uh;
uh.setInPort(12345);
uh.setOutPort(5000);
uh.listen();

PiHandler ph;
ph.setOutPort(10001);
