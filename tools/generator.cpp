#include <iostream>
#include <fstream>
#include <cstdlib>
#include <cassert>
#include <ctime>
#include <random>

int main(int argc, char *argv[])
{
    assert(argc >= 3);

    const char *out_file = argv[1];
    int n = atoi(argv[2]);
    long long max_abs = 100000000;
    if (argc >= 4)
        max_abs = (long long)atoll(argv[3]);
    unsigned seed = (argc >= 5) ? (unsigned)atoi(argv[4]) : (unsigned)time(nullptr);

    if (n < 1) n = 1;
    if (n > 1000000) n = 1000000;
    if (max_abs < 1) max_abs = 1;

    std::mt19937 gen(seed);
    std::uniform_int_distribution<long long> dist(-max_abs, max_abs);

    std::ofstream fout(out_file);
    assert(fout.is_open());

    fout << n << "\n";
    for (int i = 0; i < n; i++) {
        long long a = dist(gen);
        fout << (i ? " " : "") << a;
    }
    fout << "\n";

    fout.close();
    return 0;
}
