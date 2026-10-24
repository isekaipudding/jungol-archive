// 링크 : https://jungol.co.kr/problem/11044
#include <iostream>

using namespace std;
using ll = long long;

// 에디토리얼: https://en.wikipedia.org/wiki/Farey_sequence
/*
[힌트 소스 코드]
from fractions import Fraction
from collections.abc import Generator

def farey_sequence(n: int, descending: bool = False) -> Generator[Fraction]:
    #Print the n'th Farey sequence. Allow for either ascending or descending.
    # print(*farey_sequence(5), sep=' ')
    # 0 1/5 1/4 1/3 2/5 1/2 3/5 2/3 3/4 4/5 1
    a, b, c, d = 0, 1, 1, n
    if descending:
        a, c = 1, n - 1
    yield Fraction(a, b)
    while 0 <= c <= n:
        k = (n + b) // d
        a, b, c, d = c, d, k * c - a, k * d - b
        yield Fraction(a, b)
*/

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, k;
    cin >> n >> k;

    if (k == 1) {
        cout << "0 1";
        return 0;
    }
    if (k == 2) {
        cout << "1 " << n;
        return 0;
    }

    ll a = 0, b = 1, c = 1, d = n;

    for (int i = 0; i < k - 2; i++) {
        ll m = (n + b) / d;
        ll next_c = m * c - a;
        ll next_d = m * d - b;

        a = c;
        b = d;
        c = next_c;
        d = next_d;
    }

    cout << c << " " << d;

    return 0;
}