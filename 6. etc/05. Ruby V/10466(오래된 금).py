# 링크 : https://jungol.co.kr/problem/10466
import sys

sys.setrecursionlimit(1 << 20)
input = sys.stdin.readline

# 에디토리얼 보고 거기에 펜윅 트리 + 사건 대기줄(event queue) 추가해서 최적화를 노렸습니다.
# 저번에 방사성 섬들 문제 이것도 그렇고 Google Code Jam에는 재미있는 문제들이 많이 있네요.
# 앞으로 다른 Google Code Jam 문제들도 풀어봐야겠어요.

MOD = 10**9 + 7

# 구간 합과 단일 업데이트를 O(log N)에 처리하는 펜윅 트리
class FenwickTree:
    def __init__(self, size:int):
        self.tree:list = [0] * (size + 1)
        
    def add(self, index:int, delta:int):
        index += 1
        while index < len(self.tree):
            self.tree[index] = (self.tree[index] + delta) % MOD
            index += index & (-index)
            
    def query(self, index:int) -> int:
        index += 1
        range_sum:int = 0
        while index > 0:
            range_sum = (range_sum + self.tree[index]) % MOD
            index -= index & (-index)
        return range_sum
        
    def query_range(self, left_index:int, right_index:int) -> int:
        if left_index > right_index:
            return 0
        return (self.query(right_index) - self.query(left_index - 1)) % MOD


def old_gold_optimized(path_string:str) -> int:
    total_length:int = len(path_string)
    
    # 1. next_gt[i] : i번째 이후에 등장하는 가장 첫 번째 '>' 기호의 인덱스 O(N)
    next_gt_array:list = [-1] * total_length
    current_gt_index:int = -1
    for index in range(total_length - 1, -1, -1):
        next_gt_array[index] = current_gt_index
        if path_string[index] == '>':
            current_gt_index = index
            
    # 2. 이벤트 큐 (만료 스케줄러) : 특정 시간에 무효화될 DP 인덱스들을 저장
    expiration_queue:list = [[] for _ in range(2 * total_length + 1)]
    
    fenwick = FenwickTree(total_length)
    dp:list = [0] * total_length

    LOOKUP = {
        'o': -1,
        '<': -1,
        '=': -1,
        '>': -1
    }

    prev_prev_eq_index:int = -1
    can_be_first_gold:bool = True
    
    for i, char in enumerate(path_string):
        # 현재 시간 i에 도달하여 만료된(죽은) 과거의 dp[j] 값들을 즉시 제거
        if i < len(expiration_queue):
            for expired_j in expiration_queue[i]:
                fenwick.add(expired_j, -dp[expired_j])
                
        current_dp:int = 0
        if char == '=':
            prev_prev_eq_index = LOOKUP['=']
            
        if char in 'o.':
            # 시작점이 될 수 있는 경우 기본값 1 추가
            if can_be_first_gold:
                current_dp = (current_dp + 1) % MOD
                
            # '<' 와 'o' 제약에 따른 유효 시작점
            left_bound:int = max(LOOKUP['o'], i - 2 * (i - LOOKUP['<']) + 1)
            
            # '=' 제약 처리 : 중간 지점 강제 고정
            if LOOKUP['='] >= left_bound:
                eq_index:int = LOOKUP['=']
                target_j:int = i - 2 * (i - eq_index)
                
                # target_j가 유효 범위 내에 있고, 이전 '='을 넘지 않는다면 값 합산
                # (이벤트 큐 덕분에 중간에 '>'가 끼어있어 만료된 경우 Fenwick에서 이미 0으로 처리됨)
                if target_j >= max(left_bound, prev_prev_eq_index + 1):
                    current_dp = (current_dp + fenwick.query_range(target_j, target_j)) % MOD
                left_bound = eq_index + 1
            
            # 남은 유효 구간 [left_bound, i-1]의 살아있는 DP 합산
            if i - 1 >= left_bound:
                current_dp = (current_dp + fenwick.query_range(left_bound, i - 1)) % MOD
                
        # 현재 위치의 DP 값을 저장 및 활성화
        dp[i] = current_dp
        fenwick.add(i, current_dp)
        LOOKUP[char] = i
        
        # 현재 놓인 금 덩어리가 미래의 '>' 기호로 인해 언제 죽을지 스케줄링
        next_gt_index:int = next_gt_array[i]
        if next_gt_index != -1:
            expiration_time:int = 2 * next_gt_index - i
            if expiration_time < len(expiration_queue):
                expiration_queue[expiration_time].append(i)
                
        if char not in '>.':
            can_be_first_gold = False
            
    # S의 끝까지 모순이 없는 금 배치들만 합산
    result:int = 0
    min_last_gold_index:int = max(LOOKUP['='] + 1, LOOKUP['>'] + 1, LOOKUP['o'])
    for j in range(max(0, min_last_gold_index), total_length):
        result = (result + dp[j]) % MOD
        
    return result

T:int = int(input().rstrip())
for number in range(1, T + 1, 1):
    road:str = input().rstrip()
    print(f"Case #{number}: {old_gold_optimized(road)}")