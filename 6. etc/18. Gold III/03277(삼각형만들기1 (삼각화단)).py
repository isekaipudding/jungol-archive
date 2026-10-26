# 링크 : https://jungol.co.kr/problem/3277
import sys

input = sys.stdin.readline

# Alcuin's sequence(알퀸의 수열) 공식을 활용합니다.
# 출처 : https://oeis.org/A005044
# 해당 내용에서 FORMULA 문단에 정확히 10번째 줄에 있습니다.
# a(n) = round(n^2/48) if n is even; a(n) = round((n+3)^2/48) if n is odd. - James East, May 01 2016

def alcuin(N:int):
    if N & 1:
        return ((N + 3) * (N + 3) + 24) // 48
    else:
        return (N * N + 24) // 48

for _ in range(5):
    N:int = int(input().rstrip())
    print(alcuin(N))