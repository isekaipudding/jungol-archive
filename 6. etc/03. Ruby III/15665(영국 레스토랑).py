# 링크 : https://jungol.co.kr/problem/15665

import sys
from decimal import Decimal, getcontext, ROUND_HALF_UP

input = sys.stdin.readline
getcontext().prec = 30

# 에디토리얼 출처 : https://icpcarchive.github.io/Europe%20Contests/Northwestern%20Europe%20Regional%20Contest%20(NWERC)/2017%20Northwestern%20Europe%20Regional%20Contest/solution.pdf
# 뭐 이렇게 어려워요???ㄷㄷ 에디토리얼 보고도 모르겠네요...ㄷㄷ
# 너무 어려워서 story 추가해서 현실적으로 바꾸도록 합니다.

# 이거 실전성 있게 쓰는 방법은 각 지점마다 오전 타임, 오후 타임으로 분할해서 N, G, T를 다르게 하고
# 그 다음 1인당 평균 매출 금액을 알아내서
# "문을 닫을 때 식당 안에 있는 사람 수의 기댓값"에 1인당 평균 매출 금액을 곱하면 예상 매출 금액을 예측할 수 있어요.

# 런타임 전처리
LIMIT = 200 # N + T의 최대값이 200

fact = [0 for _ in range(LIMIT + 1)]

# 초기식 1
fact[0] = 1

# 점화식 1
for i in range(1, LIMIT + 1, 1):
    fact[i] = i * fact[i - 1]

def binomial_coefficient(n, k):
    return fact[n] // fact[k] // fact[n - k]

# [Story] Robin의 식당 세팅
# N=4(식당 안 테이블 4개), G=3(최대 3명 그룹), T=3(영업시간 3시간, 총 3팀 방문)
N, G, T = map(int, input().split())
# [Story] C = [4, 1, 3, 2] (우리 식당 테이블은 4인용, 1인용, 3인용, 2인용입니다)
C:list = list(map(int, input().split()))

for i in range(N):
    C[i] = min(C[i], G)

# 에디토리얼 1번 내용
# Sort tables by capacity(그리디 알고리즘 적용을 위한 정렬)
# [Story] 손님들은 빈자리 중 '가장 딱 맞는 작은 테이블'을 찾습니다.
# [Story] 사장님은 손님들이 고민 없이 왼쪽부터 걸어가며 앉을 수 있도록 테이블을 크기순으로 일렬로 배치합니다.
# [Story] 책상들을 아무렇게 배치하면 머리만 아프잖아요? 
# [Story] 그래서 혼밥하는 분들은 어차피 금방 나가니 맨 앞에 배치하고
# [Story] 단체 예약이면 맨 뒤에 보내도록 합니다.
C.sort()

# 에디토리얼 3번 내용
# Add t virtual tables of capacity g, holding the people leaving restaurant.
# 0-based index -> 1-based index가 되기 위해 맨 앞에 0을 추가합니다.
# [Story] 최대 3명(G)이 오는데, 처음 4인용이었던 테이블도 어차피 3명까지만 차므로 3인용으로 깎아서 생각(min 처리)합니다.
# [Story] 수학 공식이 꼬이는 걸 막기 위해, 식당 문 밖에 수용 인원 3명짜리 무한 야외 텐트(가상 테이블)를 3(T)개 설치합니다.
# [Story] 자리가 없어 쫓겨난 손님들은 집에 가는 게 아니라 이 야외 텐트에 강제로 앉힙니다.
# 배열 상태: [0(더미), 1, 2, 3, 3(실내), 3, 3, 3(야외 텐트)]
C = [0] + C + [G for _ in range(T)]

# 에디토리얼 2번 내용
# Calculate expected occupancy E(i, j) for consecutive intervals of tables between i and j, 
# conditioned upon the interval being fully occupied and the rest being empty.

# M: 실제 테이블 + 가상 테이블의 총 개수
# [Story] M = 4 + 3 = 7 (총 관리해야 할 실내외 테이블 개수)
M = N + T

# DP 테이블 정의 (W: 경우의 수, E: 사람 수 총합)
W:list = [[0 for _ in range(M + 2)] for _ in range(M + 2)]
E:list = [[0 for _ in range(M + 2)] for _ in range(M + 2)]

# 에디토리얼 4번 내용
# Dynamic programming, from smallest intervals to the longest.
# Pick the last table k occupied in an interval [i, j]. 
# Intervals [i, k-1] and [k+1, j] have been occupied before. 
# There are ({j-i}, {k-i}) ways of interleaving these two parts.

# 초기식 2 : 길이가 0인 구간(빈 구간)은 경우의 수 1개, 인원수 0명
for i in range(1, M + 2):
    W[i][i - 1] = 1
    E[i][i - 1] = 0

# 점화식 2 : 구간 DP 실행 (구간 길이 1부터 최대 T까지 증가)
for length in range(1, T + 1):
    for i in range(1, M - length + 2):
        j = i + length - 1
        
        # [i, j] 구간 내에서 가장 마지막으로 채워진 테이블 k 탐색
        # [Story] i번부터 j번 테이블까지 빈자리 없이 꽉 찬 "핫플레이스 구역"을 상상해봅시다.
        # [Story] k는 이 구역에서 "가장 늦게 들어와서 마지막 남은 빈자리를 차지한 진상 손님"이 앉은 테이블입니다.
        for k in range(i, j + 1, 1):
            # 마지막 손님 무리의 크기 범위 : C[i-1] < s <= C[k]
            # [Story] k번 손님의 인원수(s) 추리하기 
            # [Story] 왼쪽(i-1번) 테이블이 비어있는데 굳이 k번까지 걸어왔다는 건, 왼쪽 테이블보단 덩치가 컸다는 뜻입니다.
            # [Story] 하지만 k번 테이블보단 작아야 앉을 수 있죠. (C[i-1] < s <= C[k])
            TEMP = max(0, C[k] - C[i - 1])
            if TEMP == 0:
                continue
            
            # 마지막 무리의 인원수 합계 (등차수열 합)
            # 가상 테이블(k > N)은 식당을 떠난 손님이므로 0명 처리
            # [Story] k번 테이블에 앉은 손님 수의 평균 기댓값(sum_s) 구하기.
            # [Story] 핵심!! 만약 이 마지막 손님(k)이 야외 텐트(k > N, 즉 5번부터 7번까지)에 앉았다면?
            # [Story] 걔네는 쫓겨난 손님이므로 우리 식당 매상(인원수)에 1명도 포함시키면 안 됩니다(0명 처리).
            sum_s = (C[i - 1] + 1 + C[k]) * TEMP // 2 if k <= N else 0
            
            # 이항 계수로 interleave 계산
            # [Story] k번 손님이 오기 전까지, 왼쪽에 앉은 손님들과 오른쪽에 앉은 손님들이 
            # [Story] 식당 문을 열고 들어온 시간적 순서를 마구 섞어주는 작업입니다.
            left_length = k - i
            right_length = j - k
            interleave = binomial_coefficient(left_length + right_length, left_length)
            
            w_left, w_right = W[i][k - 1], W[k + 1][j]
            e_left, e_right = E[i][k - 1], E[k + 1][j]
            
            # 경우의 수 갱신
            ways = interleave * w_left * w_right * TEMP
            W[i][j] += ways
            
            # 사람 수 총합 갱신 (분배법칙 적용)
            people = interleave * (
                e_left * w_right * TEMP +
                w_left * e_right * TEMP +
                w_left * w_right * sum_s
            )
            E[i][j] += people

# 에디토리얼 5번 내용
# Use consecutive occupancies to calculate non-consecutive occupancies:
# F(k, l) is the average occupancy of the first k tables when l of those tables are occupied.
# [Story] 위에서 만든 건 빈틈없이 꽉 찬 핫플레이스 구역 단일 블록들입니다.
# [Story] 이제 진짜 현실 식당처럼 1번엔 손님이 있고, 2번은 비어있고, 3,4번은 차있는 불연속적인 배치를 계산합니다.
# FW는 경우의 수
FW:list = [[0 for _ in range(T + 1)] for _ in range(M + 1)]
FE:list = [[0 for _ in range(T + 1)] for _ in range(M + 1)]

# 초기식 3
FW[0][0] = 1

# 에디토리얼 6번 내용
# F is calculated similarly to E.

# 점화식 3
for k in range(1, M + 1, 1):
    for l in range(0, min(k, T) + 1, 1):
        
        # 경우 1 -> k번째 테이블이 비어 있는 경우 (앞선 상태 그대로 계승)
        # [Story] k번째 테이블에 텅 비어 있습니다. 
        # [Story] 그럼 그냥 어제(k-1번 테이블까지의 상황) 매출 기록을 그대로 오늘로 복사해옵니다.
        FW[k][l] += FW[k - 1][l]
        FE[k][l] += FE[k - 1][l]
        
        # 경우 2 -> k번째 테이블이 꽉 찬 블록 [i, k]의 끝점인 경우
        # [Story] k번째 테이블에 손님이 앉아 있어요!!!
        # [Story] 그럼 분명히 k번을 끝점으로 하는 꽉 찬 핫플 구역 [i, k]가 존재할 겁니다.
        for i in range(1, k + 1):
            length = k - i + 1
            
            # 이번 블록 길이가 우리가 맞춰야 할 총 점유 수(l)보다 크면 불가능
            if length > l:
                continue
            
            # 인덱스 경계 보정 -> i=1이면 앞쪽이 없으므로 기저 상태(0) 참조, 아니면 i-2 참조
            # [Story] 이 구역이 완벽히 고립되려면 바로 앞 테이블(i-1)은 무조건 비워둬야 바리케이드가 쳐집니다.
            # [Story] 그래서 이전 매출 기록은 바리케이드 앞쪽인 i-2번까지만 끌고 옵니다.
            prev_k = 0 if i == 1 else i - 2
            
            # 시간의 인터리빙 계수(조합)
            interleave = binomial_coefficient(l, length)
            
            w_block = W[i][k]
            e_block = E[i][k]
            
            fw_prev = FW[prev_k][l - length]
            fe_prev = FE[prev_k][l - length]
            
            # 경우의 수 갱신
            ways = interleave * fw_prev * w_block
            FW[k][l] += ways
            
            # 인원수 기댓값 총합 갱신(분배법칙)
            people = interleave * (fe_prev * w_block + fw_prev * e_block)
            FE[k][l] += people

# 에디토리얼 7번 내용
# Final answer is F(n + t t)– expected occupancy of the n + t tables when t of them are occupied.
# [Story] 마침내 영업 종료 (T=3시간 경과).
# [Story] 실내외 테이블 7개(M) 중 가상 텐트를 포함해 정확히 3개(T)의 테이블에 손님이 앉아 있습니다.
# [Story] (총 인원수) / (가능한 모든 방문 조합의 경우의 수) = 식당 안 평균 인원수!
result:Decimal = (Decimal(FE[M][T]) / Decimal(FW[M][T])).quantize(Decimal('0.000000000'), rounding=ROUND_HALF_UP)
print(result)



# 아래 주석 부분은 이 문제의 소스 코드를 어떻게 실전 써먹을까 고민하면서 작성한 글입니다.
"""
[외식업 매출 예측 시뮬레이션]

식당의 자산(C)은 [1인용, 2인용, 3인용, 4인용] 테이블로 고정되어 있다.
하지만 지점의 상권 특성(A/B)과 시간대(오전/오후)에 따라 
가동하는 테이블 수(N), 타겟 손님 규모(G), 방문 빈도(T), 1인당 평균 매출(객단가)을 다르게 쪼개어 시뮬레이션을 돌린다. 
이를 통해 4가지 독립된 '예상 매출'을 정밀하게 타겟팅할 수 있다.

=======================================================
▶ [A지점 - 오피스 상권] : 직장인 타겟
=======================================================
(1) 오전 런치 타임 (소규모 빠른 회전)
- 특징 -> 2~3인 단위의 직장인들이 빠르게 점심을 먹고 빠진다.
- 테이블 가동(N) = 3개 (1인용, 2인용, 4인용 오픈 / 3인용은 동선을 위해 임시 폐쇄)
- 타겟 그룹(G) = 최대 3명 (4인용 테이블도 3인용으로 상한선 min 처리)
- 방문 팀 수(T) = 4팀
- DP 연산용 C 배열 = [0(더미), 1, 2, 3(실내), 3, 3, 3, 3(가상 텐트)]
- 객단가 = 12,000원
=> [DP 알고리즘 도출] 기대 인원수 : 4.8명
=> 예상 매출 = 4.8명 * 12,000원 = 57,600원

(2) 오후 디너 타임 (부서 회식 및 접대)
- 특징: 법인카드를 사용하는 4인 단위의 묵직한 저녁 회식 위주다.
- 테이블 가동(N) = 4개 (창고에 있던 3인용까지 전면 풀가동)
- 타겟 그룹(G) = 최대 4명 
- 방문 팀 수(T) = 3팀 (테이블 점유 시간이 김)
- DP 연산용 C 배열 = [0(더미), 1, 2, 3, 4(실내), 4, 4, 4(가상 텐트)]
- 객단가 = 45,000원 (고급 요리 및 주류)
=> [DP 알고리즘 도출] 기대 인원수 : 6.5명
=> 예상 매출 = 6.5명 * 45,000원 = 292,500원

(3) 총 예상 매출 금액
=> 예상 매출 = 57,600원 + 292,500원 = 350,100원


=======================================================
▶ [B지점 - 대학가 상권] : 학생 타겟
=======================================================
(1) 오전 런치 타임 (혼밥족 및 공강 시간)
- 특징: 공강 시간에 혼자 밥을 먹거나 커플끼리 오는 경우가 압도적으로 많다.
- 테이블 가동(N) = 4개 (전부 가동)
- 타겟 그룹(G) = 최대 2명 (3, 4인용 테이블도 2명이 차지하므로 2인용으로 min 처리)
- 방문 팀 수(T) = 5팀 (혼밥 위주라 회전율이 매우 높음)
- DP 연산용 C 배열 = [0(더미), 1, 2, 2, 2(실내), 2, 2, 2, 2, 2(가상 텐트)]
- 객단가 = 8,500원 (가성비 런치 세트)
=> [DP 알고리즘 도출] 기대 인원수: 6.8명
=> 예상 매출 = 6.8명 * 8,500원 = 57,800원

(2) 오후 디너 타임 (동아리 모임 및 호프)
- 특징: 3~4인 단위의 친구들끼리 오래 앉아 술을 마신다. 혼밥석은 인기가 없다.
- 테이블 가동(N) = 3개 (1인용 테이블은 치워버리고 맥주 케그를 놓는 공간으로 활용)
- 타겟 그룹(G) = 최대 4명
- 방문 팀 수(T) = 4팀
- DP 연산용 C 배열 = [0(더미), 2, 3, 4(실내), 4, 4, 4, 4(가상 텐트)]
- 객단가 = 25,000원 (안주 및 생맥주)
=> [DP 알고리즘 도출] 기대 인원수: 7.2명
=> 예상 매출 = 7.2명 * 25,000원 = 180,000원

(3) 총 예상 매출 금액
=> 예상 매출 = 57,800원 + 180,000원 = 237,800원



만약 두 지점의 예상 매출 금액을 합하면 그 날의 예상 매출 금액을 예측할 수 있어요.
350,100원 + 237,800원 = 587,900원

만약 이 예상 매출 금액이 한달 기준(30일 기준) 평균 일 매출 금액이라면
17,637,000원 정도의 예상 매출 금액이 나옵니다.

[일일 예상 매출 산출]
A지점 오전 : 4.8명 * 12,000원 = 57,600원
A지점 오후 : 6.5명 * 45,000원 = 292,500원
A지점 합계 : 57,600원 + 292,500원 = 350,100원

B지점 오전 : 6.8명 * 8,500원 = 57,800원
B지점 오후 : 7.2명 * 25,000원 = 180,000원
B지점 합계 : 57,800원 + 180,000원 = 237,800원

두 지점 합산 일매출 : 350,100원 + 237,800원 = 587,900원

[월간 예상 매출 산출]
월 매출 (30일 기준) : 587,900원 * 30일 = 17,637,000원



이렇게 해서 PS 문제를 어떻게 실용적으로 써먹을지 고민해봤고 그 결과물은 위와 같습니다.
그 외에도 빅데이터를 활용하여 각 지점마다 예상 사람 수의 기댓값과 예상 1인당 매출 금액을 알아내서
예상 매출 금액을 계산하고 거기에 알맞은 경영 전략을 짤 수 있습니다.
"""