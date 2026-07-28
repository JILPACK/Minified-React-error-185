// Suite de Fibonacci avec memoization
fun fib(n) {
    if n <= 1 {
        return n;
    }
    return fib(n - 1) + fib(n - 2);
}

let i = 0;
while i <= 15 {
    print i;
    print fib(i);
    i = i + 1;
}
