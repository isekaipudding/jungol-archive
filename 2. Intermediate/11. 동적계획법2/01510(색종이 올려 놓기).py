# 링크 : https://jungol.co.kr/problem/1510
import sys

input = sys.stdin.readline

N:int = int(input().rstrip())
papers:list = []
for _ in range(N):
    w, h = map(int, input().split())
    # 회전이 가능하므로 항상 (작은 변, 큰 변)으로 표준화
    papers.append((min(w, h), max(w, h)))

# 작은 변 기준 오름차순, 같다면 큰 변 기준 오름차순 정렬
papers.sort(key=lambda x: (x[0], x[1]))

# i번째 색종이를 바닥(맨 아래)으로 둘 때 쌓을 수 있는 최대 장수
dp:list = [1] * N

# LIS 2차원 조건 점화식
for i in range(N):
    for j in range(i):
        # j번째 색종이가 i번째 색종이 안에 쏙 들어갈 수 있는지 확인
        if papers[j][0] <= papers[i][0] and papers[j][1] <= papers[i][1]:
            dp[i] = max(dp[i], dp[j] + 1)

print(max(dp) if N > 0 else 0)