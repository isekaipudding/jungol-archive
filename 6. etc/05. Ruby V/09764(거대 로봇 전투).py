# 링크 : https://jungol.co.kr/problem/9764
import sys
import math
import heapq

input = sys.stdin.readline

VIRTUAL_MINION_HEIGHT = 2000000000
INF = 2 * VIRTUAL_MINION_HEIGHT
LOG = 19

def get_ancestor(node:int, k:int) -> int:
    for j in range(LOG):
        if (k >> j) & 1:
            node = up_table[node][j]
    return node

def calculate_leaf(start_index:int, end_index:int, current_k_value:int) -> list:
    if start_index == end_index:
        if depth_node[start_index] < current_k_value:
            return [0, 0, 0]
        elif depth_node[start_index] == current_k_value:
            return [0, 0, 1]
        else:
            return [INF, 0, 1]
    
    distance:int = depth_node[start_index] - depth_node[end_index]
    s_mx:int = get_ancestor(start_index, distance - 1)
    
    if depth_node[start_index] <= current_k_value:
        return [0, H[s_mx], 0]
    else:
        if depth_node[s_mx] > current_k_value:
            return [INF, 0, 1]
        else:
            jump:int = depth_node[start_index] - current_k_value
            s_mi:int = get_ancestor(start_index, jump)
            return [H[s_mi], H[s_mx], 0]

def schedule_segment(start_index:int, end_index:int, current_k:int) -> None:
    if start_index == end_index:
        if current_k > depth_node[start_index]:
            return
        elif current_k == depth_node[start_index]:
            next_k = current_k + 1
        else:
            next_k = depth_node[start_index]
    else:
        if current_k >= depth_node[start_index]:
            return
        distance:int = depth_node[start_index] - depth_node[end_index]
        s_mx:int = get_ancestor(start_index, distance - 1)
        if current_k < depth_node[s_mx]:
            next_k = depth_node[s_mx]
        else:
            next_k = current_k + 1
            
    if next_k <= N + 1:
        heapq.heappush(pq, (next_k, start_index, end_index))

def merge_nodes(left_node:list, right_node:list) -> list:
    if not left_node and not right_node:
        return [0, 0, 0]
    if not left_node:
        return right_node[:]
    if not right_node:
        return left_node[:]

    l_hmi:int = left_node[0]
    l_hmx:int = left_node[1]
    l_force:int = left_node[2]
    
    r_hmi:int = right_node[0]
    r_hmx:int = right_node[1]
    r_force:int = right_node[2]

    new_hmi:int = 0
    new_hmx:int = 0
    new_force:int = 0

    required_hmi:int = r_hmi if l_hmx < r_hmi else 0

    if l_force == 0 and r_force == 0:
        new_hmi = l_hmi if l_hmi > required_hmi else required_hmi
        new_hmx = l_hmx if l_hmx > r_hmx else r_hmx
        new_force = 0
    elif l_force == 0 and r_force == 1:
        new_hmi = l_hmi if l_hmi > required_hmi else required_hmi
        new_hmx = r_hmx
        new_force = 1
    elif l_force == 1 and r_force == 0:
        new_hmi = INF if l_hmx < r_hmi else l_hmi
        new_hmx = l_hmx if l_hmx > r_hmx else r_hmx
        new_force = 1
    else:
        new_hmi = INF if l_hmx < r_hmi else l_hmi
        new_hmx = r_hmx
        new_force = 1

    return [new_hmi, new_hmx, new_force]

def update(index:int, value:list) -> None:
    index += size
    SegmentTree[index] = value
    while index > 1:
        index >>= 1
        SegmentTree[index] = merge_nodes(SegmentTree[index << 1], SegmentTree[index << 1 | 1])

def find(x:int) -> int:
    root = x
    while parent_dsu[root] != root:
        root = parent_dsu[root]
    current = x
    while current != root:
        next_node = parent_dsu[current]
        parent_dsu[current] = root
        current = next_node
    return root

def union(x:int, y:int) -> None:
    rootX = find(x)
    rootY = find(y)
    if rootX != rootY:
        parent_dsu[rootY] = rootX
        left_most[rootX] = left_most[rootX] if left_most[rootX] < left_most[rootY] else left_most[rootY]
        right_most[rootX] = right_most[rootX] if right_most[rootX] > right_most[rootY] else right_most[rootY]

N, Q = map(int, input().split())

H:list = list(map(int, input().split()))
H.append(VIRTUAL_MINION_HEIGHT)

queries:list = []
for _ in range(Q):
    queries.append(int(input().rstrip()))

parent_node:list = [N] * (N + 1)
stack_list:list = []

for i in range(N + 1):
    while stack_list and H[stack_list[-1]] < H[i]:
        parent_node[stack_list.pop()] = i
    stack_list.append(i)

up_table:list = [[N] * LOG for _ in range(N + 1)]
depth_node:list = [0] * (N + 1)

for i in range(N - 1, -1, -1):
    up_table[i][0] = parent_node[i]
    depth_node[i] = depth_node[parent_node[i]] + 1
    for j in range(1, LOG, 1):
        up_table[i][j] = up_table[up_table[i][j - 1]][j - 1]

bits:int = int(math.ceil(math.log2(N + 1)))
size:int = 1 << bits
SegmentTree:list = [[0, 0, 0] for _ in range(2 * size)]

pq = []
current_k_value:int = 1

update(0, calculate_leaf(0, N, current_k_value))
schedule_segment(0, N, current_k_value)
for i in range(size - 1, 0, -1):
    SegmentTree[i] = merge_nodes(SegmentTree[i << 1], SegmentTree[i << 1 | 1])

sorted_queries:list = sorted([(queries[i], i) for i in range(Q)], reverse=True)
minions_desc:list = sorted([(H[i], i) for i in range(N)], reverse=True)
minions_asc:list = [(H[i], i) for i in range(N)]
minions_asc.sort(key=lambda x: (x[0], -x[1]))
minion_pointer:int = 0

parent_dsu = list(range(N))
left_most = list(range(N))
right_most = list(range(N))
active_dsu = [False] * N

precalc_L = [0] * N
precalc_R = [0] * N

for h_value, index in minions_asc:
    if index > 0 and active_dsu[index - 1]:
        precalc_L[index] = left_most[find(index - 1)] - 1
    else:
        precalc_L[index] = index - 1
        
    if index < N - 1 and active_dsu[index + 1]:
        precalc_R[index] = right_most[find(index + 1)] + 1
    else:
        precalc_R[index] = index + 1
        
    active_dsu[index] = True
    if index > 0 and active_dsu[index - 1]:
        union(index, index - 1)
    if index < N - 1 and active_dsu[index + 1]:
        union(index, index + 1)

segment_ends_dict:dict = {0: N}
result:list = [0] * Q

for robot_height, index in sorted_queries:
    while minion_pointer < N and minions_desc[minion_pointer][0] >= robot_height:
        minion_index:int = minions_desc[minion_pointer][1]
        minion_pointer += 1

        left_start:int = precalc_L[minion_index] + 1
        right_end:int = precalc_R[minion_index]

        if left_start <= minion_index:
            segment_ends_dict[left_start] = minion_index
            update(left_start, calculate_leaf(left_start, minion_index, current_k_value))
            schedule_segment(left_start, minion_index, current_k_value)
            
        if minion_index + 1 <= right_end:
            segment_ends_dict[minion_index + 1] = right_end
            update(minion_index + 1, calculate_leaf(minion_index + 1, right_end, current_k_value))
            schedule_segment(minion_index + 1, right_end, current_k_value)

    while SegmentTree[1][0] > 0:
        current_k_value += 1
        
        while pq and pq[0][0] <= current_k_value:
            next_k, segment_start, segment_end = heapq.heappop(pq)
            
            if segment_ends_dict.get(segment_start) != segment_end:
                continue
            
            update(segment_start, calculate_leaf(segment_start, segment_end, current_k_value))
            schedule_segment(segment_start, segment_end, current_k_value)

    result[index] = current_k_value

for need in result:
    print(need)