# 링크 : https://jungol.co.kr/problem/8039
import sys
from collections import defaultdict

input = sys.stdin.readline

N, Q = map(int, input().split())

# 후보자별 현재 득표수(1-based index)
candidate_votes:list = [0] * (N + 1)

# key: 득표수, value: 해당 표를 가진 후보자 집합
# 여기서는 dict가 아닌 defaultdict(set)로 해야 하네요.
vote_to_candidates = defaultdict(set)
vote_to_candidates[0] = set(range(1, N + 1, 1))

for _ in range(Q):
    query:list = list(map(int, input().split()))
    cmd:int = query[0]
    
    if cmd == 0:
        # 사소한 디테일이 따로 있다면 N은 이미 총 후보자 수로 등록한 상태이니
        # 여기서는 N 대신 M으로 해당 후보의 번호를 지정하도록 합니다.
        M, K = query[1], query[2]
        vote_to_candidates[candidate_votes[M]].discard(M)
        vote_to_candidates[candidate_votes[M] + K].add(M)
        
        candidate_votes[M] += K
    if cmd == 1:
        X:int = query[1]
        candidate_set = vote_to_candidates.get(X)
        
        if candidate_set:
            sorted_candidates = sorted(candidate_set)
            print(*sorted_candidates)
        else:
            print("None")