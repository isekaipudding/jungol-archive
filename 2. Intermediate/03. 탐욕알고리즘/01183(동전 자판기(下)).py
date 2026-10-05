# 링크 : https://jungol.co.kr/problem/1183
import sys

input = sys.stdin.readline

W:int = int(input().rstrip())
coin500, coin100, coin50, coin10, coin5, coin1 = map(int, input().split())

total:int = 0
total += 500 * coin500
total += 100 * coin100
total += 50 * coin50
total += 10 * coin10
total += 5 * coin5
total += 1 * coin1

target:int = total - W

L:list = [coin500, coin100, coin50, coin10, coin5, coin1]
COUNT:list = [0, 0, 0, 0, 0, 0]
weight:list = [500, 100, 50, 10, 5, 1]

for i in range(6):
    COUNT[i] = min(L[i], target // weight[i])
    target -= weight[i] * COUNT[i]

result:list = [L[i] - COUNT[i] for i in range(6)]
print(sum(result))
print(*result)