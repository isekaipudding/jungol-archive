// 링크 : https://jungol.co.kr/problem/4640
#include <iostream>
#include <algorithm>
#include <set>

using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int q;
    cin >> q;

    set<int> s;

    while(q--) {
        char cmd;
        int n;

        cin >> cmd >> n;

        switch(cmd) {
            case 'i':
                s.insert(n);
                break;
            case 'r':
                s.erase(n);
                break;
            case 'b': {
                auto it = s.lower_bound(n);
                if (it != s.end()) {
                    cout << *it << "\n";
                }
                break;
            }
            case 's': {
                auto it = s.upper_bound(n);
                if (it != s.begin()) {
                    cout << *prev(it) << "\n";
                }
                break;
            }
        }
    }

    return 0;
}