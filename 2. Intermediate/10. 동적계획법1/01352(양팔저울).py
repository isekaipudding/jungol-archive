# 링크 : https://jungol.co.kr/problem/1352
import sys

input = sys.stdin.readline

N:int = int(input().rstrip())
weights:list = list(map(int, input().split()))

M:int = int(input().rstrip())
beads:list = list(map(int, input().split()))

dp:set = set()

# 초기식
dp.add(0)

# 점화식
for weight in weights:
    for bead in list(dp):
        dp.add(bead + weight)
        dp.add(abs(bead - weight))

result:list = []
for bead in beads:
    # 구슬의 무게가 측정 가능한 무게 집합(dp)에 존재하면 Y, 아니면 N
    if bead in dp:
        result.append("Y")
    else:
        result.append("N")

print(*result)