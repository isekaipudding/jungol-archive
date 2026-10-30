# 링크 : https://jungol.co.kr/problem/2771
import sys
import heapq
from collections import deque

input = sys.stdin.readline

# 과거에 백준에 풀었던 백준 9539번(escape) 문제를 Python 소스 코드로 변환합니다.

def solve() -> str:
    number_of_nodes, target_node = map(int, input().split())
    # 1-index로 맞추기 위해 앞에 0 추가
    HP:list = [0] + list(map(int, input().split()))
    
    adjacency_list:list = [[] for _ in range(number_of_nodes + 1)]
    for _ in range(number_of_nodes - 1):
        u, v = map(int, input().split())
        adjacency_list[u].append(v)
        adjacency_list[v].append(u)
        
    # 1번 노드에서 target_node까지의 최단 경로(Path) 탐색
    # 이 때 BFS로 합니다.
    parent_node:list = [0] * (number_of_nodes + 1)
    queue:deque = deque([1])
    parent_node[1] = -1
    
    while queue:
        current_node:int = queue.popleft()
        if current_node == target_node:
            break
        for neighbor in adjacency_list[current_node]:
            if parent_node[neighbor] == 0:
                parent_node[neighbor] = current_node
                queue.append(neighbor)
                
    # 경로 추적 및 on_path 배열 마킹
    path_nodes:list = []
    current_trace:int = target_node
    on_path:list = [False] * (number_of_nodes + 1)
    
    while current_trace != -1:
        path_nodes.append(current_trace)
        on_path[current_trace] = True
        current_trace = parent_node[current_trace]
    path_nodes.reverse()
    
    # 경로에 속하지 않는 나머지 서브트리 노드들 탐색
    # 이것도 BFS로 합니다.
    post_order_nodes:list = []
    queue.clear()
    
    for path_node in path_nodes:
        for neighbor in adjacency_list[path_node]:
            if not on_path[neighbor]:
                parent_node[neighbor] = path_node
                queue.append(neighbor)
                
    while queue:
        current_node:int = queue.popleft()
        post_order_nodes.append(current_node)
        for neighbor in adjacency_list[current_node]:
            if neighbor != parent_node[current_node] and not on_path[neighbor]:
                parent_node[neighbor] = current_node
                queue.append(neighbor)
                
    # 바텀-업(Bottom-Up) 처리를 위해 역순 정렬
    post_order_nodes.reverse()
    
    # 서브트리 병합 처리 (Small-to-Large Trick)
    # Segment 클래스 대신 (request, -gain) 튜플을 사용하여 파이썬 heapq 최적화
    priority_queues:list = [[] for _ in range(number_of_nodes + 1)]
    
    for current_node in post_order_nodes:
        required_hp:int = max(0, -HP[current_node])
        gained_hp:int = HP[current_node]
        
        # 현재 노드의 요구량(req)과 획득량(gain)을 갱신
        while priority_queues[current_node]:
            top_request, top_negative_gain = priority_queues[current_node][0]
            top_gain:int = -top_negative_gain
            
            if gained_hp <= 0 or top_request <= required_hp + gained_hp:
                heapq.heappop(priority_queues[current_node])
                required_hp = max(required_hp, top_request - gained_hp)
                gained_hp += top_gain
            else:
                break
                
        if gained_hp > 0:
            heapq.heappush(priority_queues[current_node], (required_hp, -gained_hp))
            
        # 부모 노드로 우선순위 큐 병합
        # 이것이 바로 작은 집합에서 큰 집합으로 합치는 테크닉! (Small to Large)
        parent_index:int = parent_node[current_node]
        if len(priority_queues[current_node]) > len(priority_queues[parent_index]):
            priority_queues[current_node], priority_queues[parent_index] = priority_queues[parent_index], priority_queues[current_node]
        
        for item in priority_queues[current_node]:
            heapq.heappush(priority_queues[parent_index], item)
            
    # 메인 경로(1 -> target_node) 시뮬레이션
    global_pq:list = []
    current_HP:int = HP[1]
    escaped:bool = True
    
    for i in range(len(path_nodes)):
        current_node:int = path_nodes[i]
        if current_node == target_node:
            break
            
        # 메인 경로의 노드에 누적된 서브트리 이득(pq)을 global_pq에 병합
        if len(priority_queues[current_node]) > len(global_pq):
            global_pq, priority_queues[current_node] = priority_queues[current_node], global_pq
            
        for item in priority_queues[current_node]:
            heapq.heappush(global_pq, item)
            
        # 현재 체력으로 취할 수 있는 모든 이득을 흡수
        while global_pq and global_pq[0][0] <= current_HP:
            top_request, top_negative_gain = heapq.heappop(global_pq)
            current_HP += (-top_negative_gain)
            
        # 다음 경로로 나아갈 수 있는지 검증
        if i + 1 < len(path_nodes):
            next_node:int = path_nodes[i + 1]
            required_next_hp:int = max(0, -HP[next_node])
            if current_HP < required_next_hp:
                escaped = False
                break
            current_HP += HP[next_node]
            
    if escaped:
        return "escaped"
    else:
        return "trapped"

# 테스트 케이스 T가 주어져야 하는데
# 신기하게 정올에서는 T 입력이 안 주어서 T = 1로 고정합니다.
T:int = 1
for _ in range(T):
    print(solve())