# 링크 : https://jungol.co.kr/problem/1761
import sys

input = sys.stdin.readline

# 두 숫자를 비교해서 (스트라이크, 볼) 개수를 반환합니다.
def get_strike_ball(candidate:str, query:str):
    strike, ball = 0, 0
    for i in range(3):
        if candidate[i] == query[i]:
            strike += 1
        elif candidate[i] in query:
            ball += 1
    return strike, ball

# 런타임 전처리
candidates:set = set()
for i in range(1, 10, 1):
    for j in range(1, 10, 1):
        for k in range(1, 10, 1):
            if i != j and j != k and i != k: # 서로 다른 숫자만 추가
                candidates.add(str(i) + str(j) + str(k))

N:int = int(input().rstrip())

for _ in range(N):
    M, strike_count, ball_count = map(int, input().split())
    M = str(M)
    
    TEMP = set()
    # 현재 살아남은 후보군들 중, 이번 질문의 S/B 조건과 일치하는 녀석만 TEMP에 구출
    for cand in candidates:
        s, b = get_strike_ball(cand, M)
        if s == strike_count and b == ball_count:
            TEMP.add(cand)
            
    candidates = TEMP

result:int = len(candidates)
print(result)