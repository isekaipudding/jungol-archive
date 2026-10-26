// 링크 : https://jungol.co.kr/problem/6204
#include <iostream>

using namespace std;
using ll = long long;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    ll n;
    cin >> n;

    int r = 0;

    while(n > 1) {
        if(n & 1) n--;
        else n >>= 1;
        r++;
    }

    cout << r << "\n";

    return 0;
}