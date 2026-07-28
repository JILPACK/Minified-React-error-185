// Simulation de chute libre avec table
let g = 9.81;
let h0 = 100.0;
let t = 0.0;
let dt = 0.5;

print "Chute libre depuis";
print h0;
print "metres";
print "t(s)  h(m)  v(m/s)";

while t <= 5.0 {
    let h = h0 - 0.5 * g * t * t;
    let v = g * t;
    if h < 0 {
        h = 0;
    }
    print t;
    print h;
    print v;
    t = t + dt;
}

print "Impact!";
