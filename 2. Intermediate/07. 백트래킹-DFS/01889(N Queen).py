# 링크 : https://jungol.co.kr/problem/1889
import sys

sys.setrecursionlimit(1 << 20)
input = sys.stdin.readline

def solve_n_queens(N:int) -> int:
    # 예외 처리
    if N == 1:
        return 1
    if N <= 3:
        return 0

    ALL_ONES:int = (1 << N) - 1
    half:int = N >> 1

    def dfs(col:int, ld:int, rd: int) -> int:
        # N개의 퀸이 모두 배치됨
        if col == ALL_ONES:
            return 1

        count = 0
        # 현재 행에서 배치 가능한 열 비트마스크 추출
        avail = ALL_ONES & ~(col | ld | rd)

        # 펜윅 LSB 비트 연산으로 유효한 자리만 직행
        while avail:
            bit = avail & -avail
            avail -= bit
            count += dfs(
                col | bit,
                ((ld | bit) << 1) & ALL_ONES,
                (rd | bit) >> 1
            )
        return count

    total_solutions:int = 0

    # 1. 0번 행의 왼쪽 절반(0 ~ half - 1) 탐색 후 좌우 대칭(* 2) 반영
    for c in range(half):
        bit: int = 1 << c
        total_solutions += dfs(bit, (bit << 1) & ALL_ONES, bit >> 1) * 2

    # 2. 0번 행의 정중앙에 놓는 경우
    # 수직 대칭인 해는 존재하지 않으므로, 1번 행 또한 왼쪽 절반만 탐색 후 * 2로 절삭 가능
    if N & 1:
        mid_bit = 1 << half
        ld0 = (mid_bit << 1) & ALL_ONES
        rd0 = mid_bit >> 1
        col0 = mid_bit

        # 1번 행의 후보 중 왼쪽 절반(열 인덱스 < half)만 시도
        limit_mask = (1 << half) - 1
        avail1 = limit_mask & ~(col0 | ld0 | rd0)

        mid_count = 0
        while avail1:
            b1 = avail1 & -avail1
            avail1 -= b1
            mid_count += dfs(
                col0 | b1,
                ((ld0 | b1) << 1) & ALL_ONES,
                (rd0 | b1) >> 1
            )
        total_solutions += mid_count * 2

    return total_solutions

N:int = int(input().rstrip())
print(solve_n_queens(N))