#include <iostream>
#include <fstream>
#include <cstdlib>
#include <cassert>
#include <ctime>

int main(int argc, char *argv[])
{
    assert(argc >= 3);

    const char *out_file = argv[1];
    int n = atoi(argv[2]);
    int max_abs = 1000;
    if (argc >= 4)
        max_abs = atoi(argv[3]);
    unsigned seed = (argc >= 5) ? (unsigned)atoi(argv[4]) : (unsigned)time(nullptr);
    srand(seed);

    if (n < 1) n = 1;
    if (n > 10) n = 10;
    if (max_abs < 1) max_abs = 1;

    std::ofstream fout(out_file);
    assert(fout.is_open());

    fout << n << "\n";
    for (int i = 0; i < n; i++) {
        int a = rand() % (2 * max_abs + 1) - max_abs;
        fout << (i ? " " : "") << a;
    }
    fout << "\n";

    fout.close();
    return 0;
}
