# 링크 : https://jungol.co.kr/problem/1752
import sys

input = sys.stdin.readline
sys.setrecursionlimit(1 << 20)

MOD = 1000

DP = [
    [6, -4],
    [1, 0]
]
SIZE = len(DP)

def matrix_multiply(A:list[list[int]], B:list[list[int]], size:int):
    result:list = [[0 for _ in range(size)] for _ in range(size)]
    for r in range(size):
        for c in range(size):
            TEMP = 0
            for k in range(size):
                TEMP += A[r][k] * B[k][c]
            result[r][c] = TEMP % MOD
    return result

def matrix_power(A:list[list[int]], exponent:int, size:int):
    if exponent == 0:
        return [[1 if r == c else 0 for r in range(size)] for c in range(size)]
    if exponent == 1:
        return [[A[r][c] % MOD for c in range(size)] for r in range(size)]
    
    # 절반 거듭제곱을 재귀로 구합니다.
    half_matrix = matrix_power(A, exponent >> 1, size)
    
    # 절반을 제곱하여 합칩니다.
    half_squared = matrix_multiply(half_matrix, half_matrix, size)
    
    # 지수가 홀수이면 A^e = A^(e // 2) * A^(e // 2) * A
    if exponent & 1:
        return matrix_multiply(half_squared, A, size)
    # 지수가 짝수이면 A^e = A^(e // 2) * A^(e // 2)
    else:
        return half_squared

N:int = int(input().rstrip())

matrix = matrix_power(DP, N, SIZE)

TEMP:int = (matrix[0][0] + matrix[1][1] - 1) % MOD
size:int = len(str(TEMP))
result:str = "0" * (3 - size) + str(TEMP)
print(result)


"""
(3 + root 5)^n에서 a = 3 + root 5일 때 켤레 무리수 b = 3 - root 5라고 가정합니다.
이 때 두 수의 합으로 이루어진 새로운 수열 S_n은 다음과 같습니다.
S_n = a^n + b^n = (3 + root 5)^n + (3 - root 5)^n
이항 정리에 의해 홀수 제곱항들은 모두 다 없어지므로 S_n은 항상 정수입니다.

그 다음 a + b와 ab를 구하도록 합니다.
a + b = (3 + root 5) + (3 - root 5) = 6
a * b = (3 + root 5) * (3 - root 5) = 4

이 때 a와 b는 t에 대한 이차방정식으로 표현할 수 있습니다.
t^2 - 6t + 4 = 0
이 때 t^(n-2) 곱하면 다음과 같습니다.
t^n = 6t^(n-1) + 4t^(n-2)


여기서 t = a 혹은 b이므로
a^2 = 6a - 4
b^2 = 6b - 4
이렇게 되고 자연스럽게
a^n = 6a^(n-1) - 4a^(n-2)
b^n = 6b^(n-1) - 4b^(n-2)
이렇게 될 수 있으며 두 식을 합하면
(a^n + b^n) = 6 * {a^(n-1) + b^(n-1)} - 4 * {a^(n-2) + b^(n-2)}
이 때 S_n = a^n + b^n이므로

S_n = 6 * S_(n-1) - 4 * S(n-2)

이 때 행렬로 표현하기 위해 식을 하나 더 추가합니다.
S_(n-1) = 1 * S_(n-1) + 0 * S_(n-2)

여기서 DP 행렬이 나옵니다.
DP = [
    [6, 4],
    [1, 0]
]

그 뒤 DP^n 행렬
[
    [m_00, m_01],
    [m_10, m_11]
]
여기서 대각합은 행렬의 고윳값들의 N제곱 합과 같습니다.
여기서 행렬의 고윳값은 a, b를 의미하며 여기서 -1을 해주면 원하는 답을 구할 수 있습니다.



추가로 만약 (2 + root 3)^n의 정수 부분을 구할려면
DP = [
    [4, -1],
    [1, 0]
]
이렇게 설정하면 됩니다.
"""