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

    std::sort(v, v + n);

    // arrays1 - odds, array2 - evens
    int array1[NMAX], array2[NMAX];
    int array1_size = 0, array2_size = 0;
    for (int i = 0; i < n; i++) {
        if (v[i] & 1) {
            array1[array1_size++] = v[i];
        } else {
            array2[array2_size++] = v[i];
        }
    }

    int Max = INT_MIN;
    int curr_sum = 0;
    int carry = 0;

    // these are 2 pointers towards the actually arrays
    int *odds = array1, *evens = array2;
    int odds_size = array1_size, evens_size = array2_size;

    for (int step = 0; step < n; step++) {
        if (odds_size == 0) {
            // case one - only evens left
            curr_sum = curr_sum - evens[0] + carry;
            evens++;
            evens_size--;
            carry--;
        } else if (evens_size == 0) {
            // case two - only odds left
            curr_sum = curr_sum + odds[odds_size - 1] + carry;
            odds++;
            odds_size--;
            carry++;
        } else {
            // case three - both left
            if (curr_sum + odds[odds_size - 1] > curr_sum - evens[0]) {
                curr_sum = curr_sum + odds[odds_size - 1] + carry;
                odds++;
                odds_size--;
                carry++;
            } else {
                curr_sum = curr_sum - evens[0] + carry;
                evens++;
                evens_size--;
                carry--;
            }
        }

        std::swap(odds, evens);
        std::swap(odds_size, evens_size);
        Max = std::max(Max, curr_sum);
    }

    std::cout << Max << "\n";
    return 0;
}
