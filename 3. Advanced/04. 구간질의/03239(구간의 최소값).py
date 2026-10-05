# 링크 : https://jungol.co.kr/problem/3239
import sys
import math

input = sys.stdin.readline

# None는 값이 없는 것으로 취급해줍니다.

# 바텀 업 방식의 쿼리 실행 함수
def query_min(left, right):
    # 1. 0-based 인덱스로 들어온 값을 실제 트리 리프 노드 인덱스로 변환
    left += size
    right += size
    
    result = None
    
    # 두 포인터가 교차할 때까지 (루트 방향으로 올라가며) 반복
    # 원래 이 부분은 재귀 + 분할 정복으로 해야 하는데
    # 탑-다운 -> 바텀 업으로 바뀌엇 두 포인터 알고리즘으로 해결됩니다.
    while left <= right:
        
        # 2. left가 홀수 (오른쪽 자식)일 때
        if left & 1: 
            if SegmentTree[left] is not None:
                # 튜플끼리 사전순 비교 (값 우선, 동률 시 인덱스 우선)
                if result is None or SegmentTree[left] < result:
                    result = SegmentTree[left]
            left += 1 # 현재 값 채택 후 짝수(왼쪽 자식) 위치로 이동
            
        # 3. right가 짝수 (왼쪽 자식)일 때
        if not right & 1: # (right % 2 == 0)
            if SegmentTree[right] is not None:
                if result is None or SegmentTree[right] < result:
                    result = SegmentTree[right]
            right -= 1 # 현재 값 채택 후 홀수(오른쪽 자식) 위치로 이동
            
        # 4. 부모 노드로 한 칸 점프 (비트 우측 시프트)
        left >>= 1
        right >>= 1
        
    return result

def update(index:int, value:int):
    index += size
    
    if value is None:
        SegmentTree[index] = None
    else:
        SegmentTree[index] = (value, index - size + 1)
    
    # 현재 노드가 루트 노드가 아닌 경우
    while index > 1:
        index >>= 1 # 자식 노드 -> 부모 노드로 이동
        
        # 트리 dp(바텀 업 방식)
        left_child = SegmentTree[index << 1]
        right_child = SegmentTree[index << 1 | 1]

        if left_child is None and right_child is None:
            SegmentTree[index] = None
        elif left_child is None:
            SegmentTree[index] = right_child
        elif right_child is None:
            SegmentTree[index] = left_child
        else:
            SegmentTree[index] = min(left_child, right_child)

N, Q = map(int, input().split())

bits:int = int(
    math.ceil(
        math.log2(N)
    )
)
size:int = 1 << bits
SegmentTree:list = [None for _ in range(2 * size)]

for _ in range(Q):
    query:list = list(map(int, input().split()))
    cmd:int = query[0]
    
    if cmd == 1:
        k, value = query[1], query[2]
        update(k - 1, value)
    if cmd == 2:
        s, e = query[1], query[2]
        result = query_min(s - 1, e - 1)
        if result:
            print(result[1])
    if cmd == 3:
        s, e = query[1], query[2]
        result = query_min(s - 1, e - 1)
        if result:
            index = result[1]
            update(index - 1, None)