# 링크 : https://jungol.co.kr/problem/10766
import sys
import math

input = sys.stdin.readline

# 과거 백준에 제출했던 소스 코드에서 약간 다듬어서 제출합니다.

x, p = map(float, input().split())

# 예외 처리: 환불이 없거나 이길 확률이 0이면 베팅하지 않는 것(0원)이 최선
if x == 0.0 or p == 0.0:
    print("0.00000000")
    sys.exit(0)

r:float = x / 100.0
w:float = p / 100.0
s:float = 1.0 - r
q:float = 1.0 - w

# t = q / w > 1, logt = ln(t)
logt:float = math.log(q / w)

# 편미분 연립방정식(∇E = 0)의 해석적 해 도출
ln_s:float = math.log(s)
A:float = 1.0 + ln_s * (s / r)
u:float = -ln_s

a0:float = A / logt
b0:float = (u / logt) - a0

# 단봉(Concave) 곡면이므로 극점 주변의 좁은 격자(K = 2)만 탐색해도 충분함
K:int = 2
a_lo:int = max(1, int(math.floor(a0)) - K)
a_hi:int = max(1, int(math.ceil(a0)) + K)
b_lo:int = max(1, int(math.floor(b0)) - K)
b_hi:int = max(1, int(math.ceil(b0)) + K)

# b에 대한 지수 값들을 1차원으로 미리 계산 (초월함수 중복 호출 제거)
b_range = range(b_lo, b_hi + 1)
expm1_lb = [math.expm1(logt * b) for b in b_range]

best:float = 0.0

for a in range(a_lo, a_hi + 1, 1):
    la = logt * a
    exp_neg_la = math.exp(-la)

    for i, b in enumerate(b_range):
        lab = la + logt * b

        if lab < 50.0:
            P = expm1_lb[i] / math.expm1(lab)
        else:
            # lab >= 50.0 이면 exp(-lab) < 2e-22 이므로 오버플로우 없이 즉시 계산
            elab = math.exp(-lab)
            P = (exp_neg_la - elab) / (1.0 - elab)

        value = -s * b + (a + s * b) * P
        if value > best:
            best = value

print(f"{best:.8f}")