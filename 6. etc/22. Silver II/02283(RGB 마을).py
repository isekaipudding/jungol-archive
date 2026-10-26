# 링크 : https://jungol.co.kr/problem/2283
import sys

input = sys.stdin.readline

# 백준 링크 : https://www.acmicpc.net/problem/1149

N:int = int(input().rstrip())
dp:list = [0 for _ in range(3)] # 초기식

for i in range(0, N, 1) :
    Red, Green, Blue = map(int, input().split())
    TEMP:list = [Red, Green, Blue]
    
    # for문으로 작성할 수 있으나 좀 더 직관적인 코드 해석을 위해 하드 코딩했습니다.
    # 이러면 시간 복잡도가 O(1)으로 변하게 됩니다(?)
    # 이 아래에 있는 모든 식이 바로 점화식입니다.
    TEMP[0] = min(TEMP[0]+dp[1], TEMP[0]+dp[2])
    TEMP[1] = min(TEMP[1]+dp[2], TEMP[1]+dp[0])
    TEMP[2] = min(TEMP[2]+dp[0], TEMP[2]+dp[1])
    
    dp[0] = TEMP[0]
    dp[1] = TEMP[1]
    dp[2] = TEMP[2]
        
print(min(dp))