# 링크 : https://jungol.co.kr/problem/8353
import sys
import math

input = sys.stdin.readline

# 바텀 업 방식의 구간 합 쿼리 실행 함수
def query_sum(left, right) -> int:
    left += size
    right += size
    result = 0
    
    while left <= right:
        if left & 1:
            result += SegmentTree[left]
            left += 1
        if not right & 1:
            result += SegmentTree[right]
            right -= 1
        left >>= 1
        right >>= 1
        
    return result

# 바텀 업 방식의 단일 노드 갱신 함수
def update(index, value) -> None:
    index += size
    SegmentTree[index] = value
    
    while index > 1:
        index >>= 1
        SegmentTree[index] = SegmentTree[index << 1] + SegmentTree[index << 1 | 1]

# 분리 집합(Disjoint Set)의 find 연산
def find(i) -> int:
    current = i
    while parent[current] != current:
        current = parent[current]
    
    p = i
    while p != current:
        next_node = parent[p]
        parent[p] = current
        p = next_node
        
    return current

# 자릿수 합을 구하는 함수
def digit_sum(x) -> int:
    return sum(map(int, str(x)))

N, Q = map(int, input().split())
A:list = list(map(int, input().split()))

bits:int = int(math.ceil(math.log2(N)))
size:int = 1 << bits
SegmentTree:list = [0] * (2 * size)

# 초기 트리 빌드 (O(N))
for i in range(N):
    SegmentTree[size + i] = A[i]

for i in range(size - 1, 0, -1):
    SegmentTree[i] = SegmentTree[i << 1] + SegmentTree[i << 1 | 1]

# 분리 집합 초기화
# parent[i]는 인덱스 i 이후로 값이 10 이상인(아직 변환 가능한) 가장 가까운 인덱스를 가리킵니다.
parent = list(range(N + 1))

# 초기 배열에서 이미 10 미만인 값들을 미리 다음 인덱스로 압축
# 뒤에서부터 진행해야 연쇄적인 경로 압축이 O(N)만에 깔끔하게 끝납니다.
for i in range(N - 1, -1, -1):
    if A[i] < 10:
        parent[i] = find(i + 1)

for _ in range(Q):
    query:list = list(map(int, input().split()))
    cmd:int = query[0]
    
    if cmd == 1:
        L, R = query[1] - 1, query[2] - 1
        
        # 구간 [L, R] 내에서 10 이상인 유효한 인덱스만 징검다리처럼 방문
        current = find(L)
        while current <= R:
            # 실시간 자릿수 합 계산 및 리스트 업데이트
            new_value = digit_sum(A[current])
            A[current] = new_value
            update(current, new_value)
            
            # 한 번의 갱신으로 값이 10 미만이 되었다면, 다음 유효 인덱스로 포인터 연결
            if new_value < 10:
                parent[current] = find(current + 1)
                
            current = find(current + 1)
            
    if cmd == 2:
        L, R = query[1] - 1, query[2] - 1
        print(query_sum(L, R))