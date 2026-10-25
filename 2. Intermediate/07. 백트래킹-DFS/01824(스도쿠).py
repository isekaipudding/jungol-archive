# 링크 : https://jungol.co.kr/problem/1824
import sys

sys.setrecursionlimit(1 << 20)
input = sys.stdin.readline

# 스도쿠 크기
SIZE = 9
# 1부터 9까지의 비트가 모두 켜진 마스크 (2진수: 1111111110 -> 1022)
ALL_BITS = (1 << (SIZE + 1)) - 2

def dfs(index:int) -> None:
    # 모든 빈칸을 다 채운 경우 즉시 출력 후 종료
    if index == total_blanks:
        for row in sudoku:
            print(*row)
        sys.exit(0)

    r, c, b = blanks[index]

    # 현재 빈칸(r, c)에 놓을 수 있는 유효 숫자들의 비트마스크(O(1) 연산)
    avail:int = ALL_BITS & ~(row_mask[r] | col_mask[c] | box_mask[b])

    # 놓을 수 있는 유효 비트만 펜윅 비트 연산으로 추출하여 전이
    while avail:
        bit = avail & -avail
        avail -= bit

        # 비트 위치(1 << num)로부터 원래 숫자 num 복원
        num = bit.bit_length() - 1

        # 상태 전이 (스도쿠 판 및 비트마스크 갱신)
        sudoku[r][c] = num
        row_mask[r] |= bit
        col_mask[c] |= bit
        box_mask[b] |= bit

        dfs(index + 1)

        # 백트래킹 복구
        sudoku[r][c] = 0
        row_mask[r] ^= bit
        col_mask[c] ^= bit
        box_mask[b] ^= bit

# 1. 스도쿠 판 입력
sudoku:list = [list(map(int, input().split())) for _ in range(SIZE)]

# 2. 행, 열, 3x3 박스별 사용된 숫자 비트마스크 초기화
row_mask:list = [0] * SIZE
col_mask:list = [0] * SIZE
box_mask:list = [0] * SIZE

# 빈칸 좌표 목록(r, c, box_index)
blanks:list = []

for r in range(SIZE):
    for c in range(SIZE):
        value = sudoku[r][c]
        b = (r // 3) * 3 + (c // 3)
        if value == 0:
            blanks.append((r, c, b))
        else:
            bit = 1 << value
            row_mask[r] |= bit
            col_mask[c] |= bit
            box_mask[b] |= bit

total_blanks:int = len(blanks)

dfs(0)