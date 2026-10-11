# 링크 : https://jungol.co.kr/problem/10819
import sys

input = sys.stdin.readline

# 에디토리얼 출처 : https://icpcarchive.github.io/ICPC-World-Finals/2022-ICPC-World-Finals/solutions/S.html
# 이거 에디토리얼 없이 못 풀 것 같아요... 함정이 너무 많아요.

n, c = map(int, input().split())
times = list(map(int, input().split()))
times.sort() # 무조건 오름차순 정렬

# 예외 처리 1
if n <= c:
    print(times[-1])
    sys.exit(0)

# 예외 처리 2
if c == 2:
    result = 0
    index = n - 1
    
    while index >= 3:
        # 1. 가장 빠른 두 명이 셔틀을 서는 경우 vs 2. 가장 빠른 한 명이 계속 셔틀을 서는 경우
        result += times[0] + times[index] + min(2 * times[1], times[0] + times[index - 1])
        index -= 2
        
    result += times[1]
    if index == 2:
        result += times[0] + times[2]
        
    print(result)
    sys.exit(0)
    
prefix = [0] * (n + 1)
for i in range(n):
    prefix[i+1] = prefix[i] + times[i]
    
no_pure_trip_max = (n - 2) // c

# 2차원 dp 리스트를 1차원 dp 리스트로 변환했습니다.
# 시간 복잡도는 똑같이 O(N^2)이나 공간 복잡도를 O(N^2) -> O(N)으로 최적화했습니다.
# 이러면 Python의 고질적인 오버헤드가 크게 감소하여 정말 무서운 속도로 결과가 나옵니다.
MAX_COLS = no_pure_trip_max + 1
WINDOW = c + 2 # 과거 참조가 최대 c+1 전까지 발생하므로 안전하게 c+2 롤링
INF = float('inf')

# 2차원 배열의 파편화를 막기 위해 1차원으로 길게 펴서 메모리에 할당
dp = [INF] * (WINDOW * MAX_COLS)

# 1. Base case : 남은 셔틀이 0개일 때
for i in range(2, c + 1):
    row = i - 1
    row_index = (row % WINDOW) * MAX_COLS
    # dp[i - 1][0] = cost(0, i)
    dp[row_index + 0] = times[i - 1] + prefix[0]
    
# 2. Base case : 셔틀이 축적될 때
for i in range(2, c + 1):
    row = i - 1
    row_index = (row % WINDOW) * MAX_COLS
    base_cost = times[i - 1] # 루프 불변량 추출
    
    for j in range(1, MAX_COLS):
        index = min(i, j + 1)
        index_prev_row = ((index - 1) % WINDOW) * MAX_COLS
        value = prefix[index] + dp[index_prev_row + (j - index + 1)]
        
        for k in range(index - 1, 1, -1):
            k_prev_row = ((k - 1) % WINDOW) * MAX_COLS
            cand = prefix[k] + dp[k_prev_row + (j - k + 1)]
            if cand < value: value = cand
        dp[row_index + j] = value + base_cost

# 3. N = c + 1 인 경계 구역 처리
if c < n:
    row = c
    row_index = (row % WINDOW) * MAX_COLS
    
    # 새로운 윈도우에 덮어쓸 때 반드시 가비지 값을 INF로 초기화
    for j in range(MAX_COLS): dp[row_index + j] = INF
    
    base_cost = times[c + 1 - 1]
    row_1_index = (1 % WINDOW) * MAX_COLS
    
    for j in range(MAX_COLS):
        value = prefix[1] + dp[row_1_index + j]
        limit = min(j + 1, c - 1)
        
        for k in range(2, limit + 1):
            k_row_index = (k % WINDOW) * MAX_COLS
            cand = prefix[k] + dp[k_row_index + (j - k + 1)]
            if cand < value: value = cand
        dp[row_index + j] = value + base_cost

# 4. N > c + 1 인 일반 구역(O(N^2) 전이)
for i in range(c + 2, n + 1):
    row = i - 1
    row_index = (row % WINDOW) * MAX_COLS
    
    excess_max = (n - i) // c
    base_cost = times[i - 1] 
    prev_row_c_1 = ((i - c - 1) % WINDOW) * MAX_COLS
    
    for j in range(excess_max + 1):
        dp[row_index + j] = dp[prev_row_c_1 + j + 1]
    for j in range(excess_max + 1, MAX_COLS):
        dp[row_index + j] = INF

    for k in range(1, c):
        offset = prefix[k]
        k_row = ((i - c + k - 1) % WINDOW) * MAX_COLS
        
        for j in range(k - 1, excess_max + 1):
            cand = offset + dp[k_row + (j - k + 1)]
            if cand < dp[row_index + j]:
                dp[row_index + j] = cand

    for j in range(excess_max + 1):
        dp[row_index + j] += base_cost

result_row = (n - 1) % WINDOW

print(dp[result_row * MAX_COLS + 0])

"""
[실전 가능성]
여기서 실전에 써먹을려면 다음과 같은 조건을 만족해야 합니다.
1. 최대 c개 정도 이동 가능
2. 그 비용은 c개 이동 그룹의 최대값(max(T))
3. 복귀할 때는 1개만 이동

아래는 예시 사항이며 그 외에도 다른 아이디어가 있으면 이 소스 코드를 활용해주세요.
[광산 및 터널 공사, 단선(Single-track) 철도와 광차]
지하 깊은 곳에서 채굴한 광물을 밖으로 빼내는 단선 철도 시스템입니다.
- 최대 c개 전송 : 하나의 기관차(Locomotive)가 뒤에 매달 수 있는 광차(Cart)의 최대 개수가 c개입니다.
                 물리적인 견인력의 한계입니다.
- 비용은 max(T) : 광차에는 가벼운 흙(빠른 속도 가능)이 실린 것도 있고,
                  쏟아지기 쉬운 거대한 암석(아주 천천히 이동해야 함)이 실린 것도 있습니다.
                  이들은 모두 하나의 기차로 '물리적으로 연결(Coupling)'되어 있으므로,
                  전체 기차의 속도는 가장 위험하고 무거운 광차가 견딜 수 있는 최저 속도(max(T))로 제한됩니다.
- 반환 시 1개: 광물을 다 비우고 나면, 
              다음 광물들을 캐내기 위해 기관차 1대(가장 빠른 놈)만 엔진을 최대로 켜고
              빈 차로 빠르게 갱도 안으로 복귀합니다.
"""