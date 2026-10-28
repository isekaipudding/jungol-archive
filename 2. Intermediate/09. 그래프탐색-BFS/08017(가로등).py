# 링크 : https://jungol.co.kr/problem/8017
import sys

input = sys.stdin.readline

L, N, K = map(int, input().split())
A:list = list(map(int, input().split()))

# K가 가로등 개수(N) 이하인 경우 0만 K개 출력하고 종료
if K <= N:
    # end=""를 넣어야 마지막에 불필요한 줄바꿈이 한 번 더 들어가지 않습니다.
    print("0\n" * K, end="")
else:
    # 문자열 곱셈에는 반드시 * 연산자가 들어가야 합니다.
    result:list = ["0\n" * N]
    needed:int = K - N

    limits:list = []

    # 왼쪽 끝 구간 [0, A[0]]
    if A[0] > 0:
        limits.append(A[0])

    # 오른쪽 끝 구간 [A[-1], L]
    if L > A[-1]:
        limits.append(L - A[-1])

    # 가로등 사이의 내부 구간들
    for i in range(N - 1):
        gap = A[i + 1] - A[i]
        limit1 = (gap - 1) // 2
        limit2 = gap // 2
        if limit1 > 0:
            limits.append(limit1)
        if limit2 > 0:
            limits.append(limit2)

    # 한계치 오름차순 정렬(투 포인터 탐색을 위함)
    limits.sort()
    m:int = len(limits)
    pointer:int = 0
    d:int = 1

    # 투 포인터
    while needed > 0 and pointer < m:
        # 현재 거리 d보다 작은 한계치(이미 파동이 끝난 구간)는 포인터를 넘김
        while pointer < m and limits[pointer] < d:
            pointer += 1

        # d 이상 도달 가능한 활성 구간의 개수
        count = m - pointer
        if count == 0:
            break

        # 필요한 개수(needed)와 현재 거리 d에서 생성 가능한 개수(count) 중 최솟값 채택
        take = min(count, needed)
        result.append((str(d) + "\n") * take)
        needed -= take
        d += 1

    print("".join(result), end="")