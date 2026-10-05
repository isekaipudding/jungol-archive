# 링크 : https://jungol.co.kr/problem/1156
import sys

input = sys.stdin.readline

def is_possible(limit:int) -> bool:
    count = 1
    current_sum = 0
    for pages in L:
        if current_sum + pages > limit:
            count += 1
            current_sum = pages
        else:
            current_sum += pages
    return count <= K

def parametric_search():
    lo, hi = max(L), sum(L)
    best = hi
    while lo <= hi:
        mid = (lo + hi) // 2
        if is_possible(mid):
            best = mid
            hi = mid - 1
        else:
            lo = mid + 1
    return best

M, K = map(int, input().split())
L:list = list(map(int, input().split()))

result:list = []
current_sum:int = 0
remain_scribes:int = K - 1

best:int = parametric_search()

for i in range(M - 1, -1, -1):
    if i + 1 == remain_scribes:
        result.append("/")
        result.append(L[i])
        remain_scribes -= 1
        current_sum = 0
        continue

    if current_sum + L[i] > best:
        result.append("/")
        result.append(L[i])
        current_sum = L[i]
        remain_scribes -= 1
    else:
        result.append(L[i])
        current_sum += L[i]

result.reverse()

print(*result)