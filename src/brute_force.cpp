#include <iostream>
// #include <fstream>
#include <algorithm>
#include <assert.h>
#include <stdio.h>
#include <climits>

// std::ifstream fin("tasks.in");
// std::ofstream fout("tasks.out");
constexpr int NMAX = 1e6 + 2;
int n, v[NMAX];
int permutation[NMAX];
int main()
{
    std::cin >> n;
    for (int i = 0; i < n; i++) {
        std::cin >> v[i];
        permutation[i] = i;
    }

    assert(n > 0);

    int Max = INT_MIN;

    do {
        int curr = 0;
        int plus = 0;
        for (int i = 0; i < n; i++) {
            curr += ((v[permutation[i]] + plus) & 1 ? 1 : -1) * (v[permutation[i]] + plus);

            plus = plus + ((v[permutation[i]] + plus) & 1 ? -1 : 1);

            Max = std::max(Max, curr);
        }
    } while (std::next_permutation(permutation, permutation + n));

    std::cout << Max << "\n";

    return 0;
}
