# 링크 : https://jungol.co.kr/problem/3297
import sys
import math

input = sys.stdin.readline

# 바텀 업 방식의 구간 합 쿼리 실행 함수
def query_sum(left, right) -> int:
    # 1. 0-based 인덱스로 들어온 값을 실제 트리 리프 노드 인덱스로 변환
    left += size
    right += size
    
    result = 0  # 덧셈의 항등원인 0으로 초기화
    
    # 두 포인터가 교차할 때까지 (루트 방향으로 올라가며) 반복
    while left <= right:
        # 2. left가 홀수 (오른쪽 자식)일 때
        if left & 1: 
            result += SegmentTree[left]
            left += 1 # 현재 값 채택 후 짝수(왼쪽 자식) 위치로 이동
            
        # 3. right가 짝수 (왼쪽 자식)일 때
        if not right & 1: # (right % 2 == 0)
            result += SegmentTree[right]
            right -= 1 # 현재 값 채택 후 홀수(오른쪽 자식) 위치로 이동
            
        # 4. 부모 노드로 한 칸 점프 (비트 우측 시프트)
        left >>= 1
        right >>= 1
        
    return result

def update(index, value) -> None:
    index += size
    
    SegmentTree[index] = value
    
    # 현재 노드가 루트 노드가 아닌 경우
    while index > 1:
        index >>= 1 # 자식 노드 -> 부모 노드로 이동
        
        # 트리 dp(바텀 업 방식) - 두 자식의 합을 부모에 저장
        SegmentTree[index] = SegmentTree[index << 1] + SegmentTree[index << 1 | 1]

N:int = int(input().rstrip())
A:list = list(map(int, input().split()))
M:int = int(input().rstrip())

# 세그먼트 트리 크기 계산 및 초기화
bits:int = int(math.ceil(math.log2(N)))
size:int = 1 << bits

# 덧셈이므로 0으로 초기화
SegmentTree: list = [0] * (2 * size)

# 초기 배열 트리 리프 노드에 삽입
for i in range(N):
    SegmentTree[size + i] = A[i]

# 바텀-업으로 초기 트리 빌드 (O(N))
for i in range(size - 1, 0, -1):
    SegmentTree[i] = SegmentTree[i << 1] + SegmentTree[i << 1 | 1]

for _ in range(M):
    query = list(map(int, input().split()))
    cmd = query[0]
    
    if cmd == 1:
        index, value = query[1], query[2]
        # 입력은 1-based index이므로 0-based로 변환
        update(index - 1, value)
        
    elif cmd == 2:
        start, end = query[1], query[2]
        # 입력은 1-based index이므로 0-based로 변환
        print(query_sum(start - 1, end - 1))