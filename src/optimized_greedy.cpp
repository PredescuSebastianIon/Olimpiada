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
long long array1[NMAX], array2[NMAX];
long long n, v[NMAX];
bool marked[NMAX];
int main(void)
{
    std::cin >> n;
    for (long long i = 0; i < n; i++) {
        std::cin >> v[i];
    }

    
    assert(n > 0);
    
    std::sort(v, v + n);
    
    // arrays1 - odds, array2 - evens
    long long array1_size = 0, array2_size = 0;
    for (long long i = 0; i < n; i++) {
        if (v[i] & 1) {
            array1[array1_size++] = v[i];
        } else {
            array2[array2_size++] = v[i];
        }
    }
    
    long long Max = LLONG_MIN;
    long long curr_sum = 0;
    long long carry = 0;
    
    // these are 2 polong longers towards the actually arrays
    long long *odds = array1, *evens = array2;
    long long odds_size = array1_size, evens_size = array2_size;
    
    // return 0;
    for (int step = 0; step < n; step++) {
        
        if (odds_size == 0) {
            // case one - only evens left
            curr_sum = curr_sum - evens[0] + carry;
            evens++;
            evens_size--;
            carry--;
        } else if (evens_size == 0) {
            // case two - only odds left
            curr_sum = curr_sum + odds[odds_size - 1] - carry;
            odds_size--;
            carry++;
        } else {
            // case three - both left
            if (odds[odds_size - 1] - carry > -evens[0] + carry) {
                curr_sum = curr_sum + odds[odds_size - 1] - carry;
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
