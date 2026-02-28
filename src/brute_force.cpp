#include <iostream>
// #include <fstream>
#include <algorithm>
#include <assert.h>
#include <stdio.h>
#include <climits>

#define sign(x) ((x) & 1 ? 1 : -1)

// std::ifstream fin("tasks.in");
// std::ofstream fout("tasks.out");
constexpr int NMAX = 1e6 + 2;
int n;
long long permutation[NMAX], v[NMAX];
int main()
{
    std::cin >> n;
    for (int i = 0; i < n; i++) {
        std::cin >> v[i];
        permutation[i] = i * 1LL;
    }

    assert(n > 0);

    long long Max = LLONG_MIN;

    do {
        long long curr = 0;
        long long plus = 0;
        for (int i = 0; i < n; i++) {
            curr += sign(v[permutation[i]] + plus) * (v[permutation[i]] + plus);

            plus = plus + sign(v[permutation[i]] + plus);

            Max = std::max(Max, curr);
        }
    } while (std::next_permutation(permutation, permutation + n));

    std::cout << Max << "\n";

    return 0;
}
