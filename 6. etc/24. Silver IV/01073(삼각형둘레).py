# 링크 : https://jungol.co.kr/problem/1073
import sys

input = sys.stdin.readline

N:int = int(input().rstrip())
sides:list = list(map(int, input().split()))

sides.sort(reverse=True)

# 그리디 알고리즘
for i in range(N - 2):
    z, y, x = sides[i], sides[i + 1], sides[i + 2]
    if x + y > z:
        print(x + y + z)
        sys.exit(0)

print(0)