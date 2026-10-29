# 링크 : https://jungol.co.kr/problem/10906
import sys

input = sys.stdin.readline

# 에디토리얼 : https://storage.googleapis.com/files.icpc.jp/championship2024/analysis.pdf

def solve():
    n = int(input().rstrip())
    a = list(map(int, input().split()))
    
    value = -1
    k = -1
    for i in range(n):
        if a[i] > value:
            value = a[i]
            k = i
    
    if k < n - 1:
        t = a[k] - a[k + 1]
        s = a[k] - (t + 1)
        
        if s < 0:
            return -1
        
        y = (((1 << s) - 1) << (t + 2)) | ((1 << (t + 1)) - 1)
        x = y - k
    
    else:
        y = (1 << a[-1]) - 1
        x = y - (n - 1)
    
    if x < 0:
        return -1

    for i in range(n):
        if (x + i).bit_count() != a[i]:
            return -1
    
    return x

T:int = int(input().rstrip())

for _ in range(T):
    print(solve())