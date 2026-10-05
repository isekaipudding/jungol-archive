# 링크 : https://jungol.co.kr/problem/8893
import sys

input = sys.stdin.readline
sys.setrecursionlimit(1 << 20)

MOD = 1_000_000_007

FIBONACCI = [
    [1, 1],
    [1, 0]
]
SIZE = len(FIBONACCI)

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

while True:
    N:int = int(input().rstrip())
    if N == -1:
        break
    
    matrix = matrix_power(FIBONACCI, N, SIZE)
    
    print(matrix[0][1])