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
bool marked[NMAX];
int main()
{
    std::cin >> n;
    for (int i = 0; i < n; i++) {
        std::cin >> v[i];
    }

    assert(n > 0);

    int Max = INT_MIN;
    int curr_sum = 0;

    for (int i = 0; i < n; i++) {
        int poz = -1, curr_max = INT_MIN;
        for (int j = 0; j < n; j++) {
            if (marked[j])
                continue;
            
            if (curr_sum + (v[j] & 1 ? 1 : -1) * v[j] > curr_max) {
                curr_max = curr_sum + (v[j] & 1 ? 1 : -1) * v[j];
                poz = j;
            }
        }

        curr_sum = curr_max;
        marked[poz] = true;
        for (int j = 0; j < n; j++) {
            if (marked[j])
                continue;
            
            v[j] += (v[poz] & 1 ? -1 : 1);
        }

        Max = std::max(Max, curr_sum);
    }

    std::cout << Max << "\n";
    return 0;
}
