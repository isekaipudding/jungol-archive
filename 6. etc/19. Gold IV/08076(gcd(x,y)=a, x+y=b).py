# 링크 : https://jungol.co.kr/problem/8076
import sys

input = sys.stdin.readline

Q:int = int(input().rstrip())
for _ in range(Q):
    a, b = map(int, input().split())
    
    """
    gcd(x, y) = a이므로 x = ma, y = na
    x + y = b
    ma + na = b
    (m + n)a = b
    따라서 b의 약수 중에서 반드시 a가 들어가야 한다.
    """
    
    result:int = 1
    
    # 만약 b % a가 0이 아닌 경우 성립할 수 없음
    if b % a:
        result = 0
    
    # 만약 a == b이면 m + n = 1이 되며
    # m + n을 만족하는 자연수 쌍 (m, n)는 존재하지 않으므로
    # 성립할 수 없음
    if a == b:
        result = 0
    
    print(result)