# 링크 : https://jungol.co.kr/problem/11567
import sys
from collections import deque

input = sys.stdin.readline

# 이게 에디토리얼 없이 순수 해결이 되네...?

K, N = map(int, input().split())

# 초기식은 (1, K, K^2 + K)로 합니다.
# 이 때 (1, 0, 0)에서 시작하여 (1, 0, K) -> (1, K, K^2 + K)로 유도되었어요.
L:list = [(1, K, K * K + K)]

queue:deque = deque(L)

# 중복을 방지해야 하므로 집합 S를 선언합니다.
S:set = set([1, K, K * K + K])

while queue :
    # 만약 결과 리스트의 개수가 N개가 되면 탈출합니다.
    if len(L) >= N :
        break
    a, b, c = queue.popleft()
    
    # 여기가 핵심! 중복 검사를 하고 중복되지 않으면 결과 리스트에 추가하고 집합에도 추가합니다.
    if a not in S and b not in S and c not in S :
        L.append((a, b, c))
        S.update([a, b, c])
    
    # 여기가 핵심!
    # a^2 + b^2 + c^2 = k(ab + bc + ca) + 1에서 a에 관한 2차방정식 형태로 바꾸면
    # a^2 - k(b + c)a + (b^2 + c^2 - kbc - 1) = 0이 되죠
    # 거기서 a1 + a2 = k(b + c)이고요. a2는 정수이므로 a2 = a라고 가정하면
    # a1 = k(b + c) - a가 됩니다.
    # 따라서 (a, b, c) -> (a1, b, c) -> (k(b + c) - a, b, c)가 됩니다.
    # 이 때 혹시나 해서 k(b + c) - a가 0 이하의 정수가 될 수도 있으니 조건문을 추가합니다.
    # 그리고 같은 원리로 b, c도 적용하여 너비 우선 탐색 형식으로 합니다.
    if K * (b + c) - a > 0 :
        queue.append((K * (b + c) - a, b, c))
    if K * (c + a) - b > 0 :
        queue.append((a, K * (c + a) - b, c))
    if K * (a + b) - c > 0 :
        queue.append((a, b, K * (a + b) - c))

for i in range(N) :
    result:list = [L[i][0], L[i][1], L[i][2]]
    result.sort()
    print(*result)