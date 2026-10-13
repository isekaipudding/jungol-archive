# 링크 : https://jungol.co.kr/problem/2255
import sys

input = sys.stdin.readline

# 이거 보니까 순열 사이클 + 유클리드 호제법을 같이 활용해야 하는 문제이네요.
def cycle(start):
    current = start
    length = 0
    
    while not visited[current]:
        visited[current] = True
        current = L[current]
        length += 1
    
    return length

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

N:int = int(input().rstrip())
L:list = [0] + list(map(int, input().split()))

visited:list = [False] * (N + 1)

LCM = 1

for i in range(1, N + 1, 1):
    if not visited[i]:
        cycle_length = cycle(i)
        
        LCM = (LCM * cycle_length) // gcd(LCM, cycle_length)

print(LCM)