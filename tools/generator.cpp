#include <iostream>
#include <fstream>
#include <assert.h>

int main(int argc, char *argv[])
{
    assert(argc > 1);

    char *out_file = argv[1];
    int n = atoi(argv[2]);


    std::ofstream fout(out_file);


    // start generating random tests

    fout.close();

    return 0;
}
