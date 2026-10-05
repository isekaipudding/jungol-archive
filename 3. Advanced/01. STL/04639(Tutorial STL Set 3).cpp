// 링크 : https://jungol.co.kr/problem/4639
#include <iostream>
#include <algorithm>
#include <set>

using namespace std;

int main() {
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
            case 'f': {
                auto it = s.find(n);
                if (it == s.end()) {
                    cout << "NOPE" << "\n";
                    break;
                }
                if (s.size() == 1) {
                    cout << "UNIQUE" << "\n";
                    break;
                }

                if (it == s.begin()) {
                    cout << *next(it) << "\n";
                }
                else if (next(it) == s.end()) {
                    cout << *prev(it) << "\n";
                }
                else {
                    int left = *prev(it);
                    int right = *next(it);

                    if (n - left <= right - n) {
                        cout << left << "\n";
                    } else {
                        cout << right << "\n";
                    }
                }
                break;
            }
        }
    }

    return 0;
}