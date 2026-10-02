# 링크 : https://jungol.co.kr/problem/4243
import sys
from bisect import bisect_left, bisect_right
from heapq import heapify, heappop, heappush

sys.setrecursionlimit(1 << 20)

input = sys.stdin.readline

# 우와... 이걸 그래프 이론으로 끌고 와서 퍼시스턴스 세그먼트 트리로 해결한다고???
# 진짜 세상에는 나보다 훨씬 뛰어난 천외천이 많구나...ㄷㄷ

INF = 10 ** 9

def get_order(heights_array:list) -> list:
    total_buildings:int = len(heights_array)
    
    # depth_levels[i]: i에서 끝나는 최장 감소 부분수열의 길이
    lds_tails:list = []
    depth_levels:list = []
    indices_by_depth:list = [[]]
    heights_by_depth:list = [[]]
    
    for index, height in enumerate(heights_array):
        depth:int = bisect_left(lds_tails, -height)
        if depth == len(lds_tails):
            lds_tails.append(-height)
            indices_by_depth.append([])
            heights_by_depth.append([])
        else:
            lds_tails[depth] = -height
        depth += 1
        depth_levels.append(depth)
        indices_by_depth[depth].append(index)
        heights_by_depth[depth].append(height)

    # 위치 기준 / 높이 기준 퍼시스턴스 세그먼트 트리(Persistent Segment Tree)
    tree_size:int = 1 << (total_buildings - 1).bit_length()
    tree_capacity:int = 1 + 2 * total_buildings * tree_size.bit_length()
    left_child:list = [0] * tree_capacity
    right_child:list = [0] * tree_capacity
    value_array:list = [0] * tree_capacity
    used_nodes_count:int = 1

    def update(old_node:int, target_index:int, update_value:int) -> int:
        nonlocal used_nodes_count
        root_node:int = used_nodes_count
        left_bound:int = 0
        right_bound:int = tree_size
        while True:
            new_node:int = used_nodes_count
            used_nodes_count += 1
            left_child[new_node] = left_child[old_node]
            right_child[new_node] = right_child[old_node]
            old_value:int = value_array[old_node]
            value_array[new_node] = old_value if old_value > update_value else update_value
            if right_bound - left_bound == 1:
                break
            middle_bound:int = (left_bound + right_bound) >> 1
            if target_index < middle_bound:
                old_node = left_child[old_node]
                left_child[new_node] = used_nodes_count
                right_bound = middle_bound
            else:
                old_node = right_child[old_node]
                right_child[new_node] = used_nodes_count
                left_bound = middle_bound
        return root_node

    roots_by_index:list = [0]
    for index, height in enumerate(heights_array):
        roots_by_index.append(update(roots_by_index[-1], height - 1, depth_levels[index]))
        
    index_by_height:list = [0] * (total_buildings + 1)
    for index, height in enumerate(heights_array):
        index_by_height[height] = index
        
    roots_by_height:list = [0]
    for height in range(total_buildings, 0, -1):
        index:int = index_by_height[height]
        roots_by_height.append(update(roots_by_height[-1], index, depth_levels[index]))

    def query(current_node:int, query_left:int, query_right:int) -> int:
        if query_left >= query_right:
            return 0
        left_bound:int = 0
        right_bound:int = tree_size
        while True:
            if query_left <= left_bound and right_bound <= query_right:
                return value_array[current_node]
            middle_bound:int = (left_bound + right_bound) >> 1
            if query_right <= middle_bound:
                current_node = left_child[current_node]
                right_bound = middle_bound
            elif query_left >= middle_bound:
                current_node = right_child[current_node]
                left_bound = middle_bound
            else:
                break
                
        return_value:int = 0
        child_node:int = left_child[current_node]
        current_left:int = left_bound
        current_right:int = middle_bound
        while query_left > current_left:
            current_middle:int = (current_left + current_right) >> 1
            if query_left < current_middle:
                child_value:int = value_array[right_child[child_node]]
                if child_value > return_value:
                    return_value = child_value
                child_node = left_child[child_node]
                current_right = current_middle
            else:
                child_node = right_child[child_node]
                current_left = current_middle
        if value_array[child_node] > return_value:
            return_value = value_array[child_node]
            
        child_node = right_child[current_node]
        current_left = middle_bound
        current_right = right_bound
        while query_right < current_right:
            current_middle = (current_left + current_right) >> 1
            if query_right > current_middle:
                child_value = value_array[left_child[child_node]]
                if child_value > return_value:
                    return_value = child_value
                child_node = right_child[child_node]
                current_left = current_middle
            else:
                child_node = left_child[child_node]
                current_right = current_middle
        if value_array[child_node] > return_value:
            return_value = value_array[child_node]
            
        return return_value

    sparse_table:list = [None] * len(indices_by_depth)
    topological_rank:list = [0] * total_buildings
    max_previous_rank:list = [0] * total_buildings

    def compare(i:int, j:int) -> int:
        if i == j:
            return 0
        # 가장 큰 선행 번호만 달라도 즉시 비교하여 O(log^2 N) 오버헤드 멸망
        if max_previous_rank[i] != max_previous_rank[j]:
            return -1 if max_previous_rank[i] < max_previous_rank[j] else 1
            
        sign:int = 1
        if i > j:
            i, j = j, i
            sign = -1
            
        height_i:int = heights_array[i]
        height_j:int = heights_array[j]
        
        # 선행 정점 집합의 차이에 해당하는 두 직사각형 구간 최댓값 쿼리
        depth_i:int = query(roots_by_index[i], height_i, height_j - 1)
        depth_j:int = query(roots_by_height[total_buildings - height_j], i + 1, j)
        
        if depth_i != depth_j:
            return sign if depth_i > depth_j else -sign
        if not depth_i:
            return -sign
            
        previous_indices:list = indices_by_depth[depth_i]
        previous_heights:list = heights_by_depth[depth_i]
        sparse_matrix:list = sparse_table[depth_i]
        
        left_bound_i:int = bisect_right(previous_heights, height_i)
        right_bound_i:int = min(bisect_left(previous_indices, i), bisect_left(previous_heights, height_j))
        log_value:int = (right_bound_i - left_bound_i).bit_length() - 1
        sparse_row:list = sparse_matrix[log_value]
        max_rank_i:int = max(sparse_row[left_bound_i], sparse_row[right_bound_i - (1 << log_value)])
        
        left_bound_j:int = max(bisect_right(previous_indices, i), bisect_right(previous_heights, height_j))
        right_bound_j:int = bisect_left(previous_indices, j)
        log_value = (right_bound_j - left_bound_j).bit_length() - 1
        sparse_row = sparse_matrix[log_value]
        max_rank_j:int = max(sparse_row[left_bound_j], sparse_row[right_bound_j - (1 << log_value)])
        
        return sign if max_rank_i > max_rank_j else -sign

    def custom_merge_sort(array:list, left_index:int, right_index:int):
        if left_index >= right_index:
            return
            
        mid_index:int = (left_index + right_index) >> 1
        custom_merge_sort(array, left_index, mid_index)
        custom_merge_sort(array, mid_index + 1, right_index)
        
        temp_list:list = []
        left_pointer:int = left_index
        right_pointer:int = mid_index + 1
        
        while left_pointer <= mid_index and right_pointer <= right_index:
            x:int = array[left_pointer]
            y:int = array[right_pointer]
            
            # 기존 compare 함수의 -1, 0, 1 반환값을 직접 평가 (0 이하이면 x가 우선순위)
            if compare(x, y) <= 0:
                temp_list.append(x)
                left_pointer += 1
            else:
                temp_list.append(y)
                right_pointer += 1
                
        while left_pointer <= mid_index:
            temp_list.append(array[left_pointer])
            left_pointer += 1
        while right_pointer <= right_index:
            temp_list.append(array[right_pointer])
            right_pointer += 1
            
        for copy_index in range(len(temp_list)):
            array[left_index + copy_index] = temp_list[copy_index]

    # 낮은 레벨부터 사전순 위상 번호 부여
    current_rank_value:int = 0
    for current_depth in range(1, len(indices_by_depth)):
        current_layer_indices:list = indices_by_depth[current_depth]
        if current_depth > 1:
            previous_indices:list = indices_by_depth[current_depth - 1]
            previous_heights:list = heights_by_depth[current_depth - 1]
            sparse_matrix:list = sparse_table[current_depth - 1]
            for index in current_layer_indices:
                left_bound_index:int = bisect_right(previous_heights, heights_array[index])
                right_bound_index:int = bisect_left(previous_indices, index)
                log_value:int = (right_bound_index - left_bound_index).bit_length() - 1
                sparse_row:list = sparse_matrix[log_value]
                max_previous_rank[index] = max(sparse_row[left_bound_index], sparse_row[right_bound_index - (1 << log_value)])
                
        # 객체 생성 없는 순수 포인터 교환 방식의 병합 정렬 실행
        # 원본 배열(인덱스 오름차순)이 망가지면 이진 탐색(bisect)이 고장나므로, 복사본을 만들어 정렬합니다.
        sorted_order:list = current_layer_indices[:]
        custom_merge_sort(sorted_order, 0, len(sorted_order) - 1)
        
        for index in sorted_order:
            topological_rank[index] = current_rank_value
            current_rank_value += 1
            
        sparse_matrix = [[topological_rank[index] for index in current_layer_indices]]
        intervalue_width:int = 1
        while 2 * intervalue_width <= len(current_layer_indices):
            sparse_row = sparse_matrix[-1]
            sparse_matrix.append([max(sparse_row[index], sparse_row[index + intervalue_width]) for index in range(len(current_layer_indices) - 2 * intervalue_width + 1)])
            intervalue_width *= 2
        sparse_table[depth_levels[current_layer_indices[0]]] = sparse_matrix
        
    return topological_rank


def min_shooting_buildings(heights_array:list, topological_rank:list, players:int=2) -> list:
    total_buildings:int = len(heights_array)
    tree_size:int = 1 << (total_buildings - 1).bit_length()
    max_limit:int = total_buildings + 1
    
    min_segment_tree:list = [max_limit] * (tree_size * 2)
    min_segment_tree[tree_size:tree_size+total_buildings] = heights_array
    for index in range(tree_size - 1, 0, -1):
        min_segment_tree[index] = min(min_segment_tree[2*index], min_segment_tree[2*index+1])
        
    index_by_height:list = [0] * (total_buildings + 1)
    for index, height in enumerate(heights_array):
        index_by_height[height] = index
        
    previous_target:list = [-1] * (total_buildings + 1)
    next_target:list = [total_buildings] * (total_buildings + 1)
    current_right_target:int = total_buildings
    current_min_height:int = max_limit
    
    # 위상 정렬 기반의 지연 개방형 힙(Lazy Topological Heap)
    lazy_target_heap:list = []
    
    # 출차수가 0인 정점은 현재 수열의 뒤쪽 최솟값들이다.
    for index in range(total_buildings - 1, -1, -1):
        if heights_array[index] < current_min_height:
            current_min_height = heights_array[index]
            next_target[index] = current_right_target
            previous_target[current_right_target] = index
            current_right_target = index
            lazy_target_heap.append((-topological_rank[index], index))
    heapify(lazy_target_heap)
    
    height_thresholds:list = heights_array + [max_limit]
    
    def remove_node(target_index:int):
        tree_node:int = target_index + tree_size
        min_segment_tree[tree_node] = max_limit
        tree_node >>= 1
        while tree_node:
            min_segment_tree[tree_node] = min(min_segment_tree[2*tree_node], min_segment_tree[2*tree_node+1])
            tree_node >>= 1
            
        left_target:int = previous_target[target_index]
        right_target:int = next_target[target_index]
        height_threshold:int = height_thresholds[right_target]
        start_index:int = left_target + 1
        
        # 건물을 지운 뒤 새롭게 노출된 타겟(출차수 0)들을 찾아 힙에 삽입
        while start_index < target_index:
            query_left:int = start_index + tree_size
            query_right:int = target_index + tree_size
            min_found_height:int = max_limit
            while query_left < query_right:
                if query_left & 1:
                    if min_segment_tree[query_left] < min_found_height:
                        min_found_height = min_segment_tree[query_left]
                    query_left += 1
                if query_right & 1:
                    query_right -= 1
                    if min_segment_tree[query_right] < min_found_height:
                        min_found_height = min_segment_tree[query_right]
                query_left >>= 1
                query_right >>= 1
            if min_found_height >= height_threshold:
                break
                
            new_target_index:int = index_by_height[min_found_height]
            if left_target >= 0:
                next_target[left_target] = new_target_index
            previous_target[new_target_index] = left_target
            left_target = new_target_index
            heappush(lazy_target_heap, (-topological_rank[new_target_index], new_target_index))
            start_index = new_target_index + 1
            
        if left_target >= 0:
            next_target[left_target] = right_target
        previous_target[right_target] = left_target

    result:list = []
    
    # PLAYERS(다중 워커 스케줄러)를 우선순위 큐 로직에 완벽히 통합
    while lazy_target_heap:
        extracted_priorities:list = []
        available_targets:int = len(lazy_target_heap)
        shooters_used:int = min(available_targets, players)
        
        for _ in range(shooters_used):
            _, target_index = heappop(lazy_target_heap)
            extracted_priorities.append(target_index)
            
        turn_heights:list = []
        for target_index in extracted_priorities:
            turn_heights.append(heights_array[target_index])
            remove_node(target_index)
            
        while len(turn_heights) < players:
            turn_heights.append(max_limit)
            
        result.append(tuple(turn_heights))
        
    # 마지막 발사부터 결정했으므로 시간의 흐름을 원래대로 뒤집는다.
    result.reverse()
    return result


buildings_count:int = int(input().rstrip())
buildings:list = list(map(int, input().split()))

PLAYERS:int = 2

# 1. 퍼시스턴스 세그먼트 트리 + 희소 배열로 위상 정렬을 구한다.
computed_rank:list = get_order(buildings)
# 2. 지연 개방형 힙 스케줄러로 다중 플레이어 시뮬레이션을 수행한다.
result:list = min_shooting_buildings(buildings, computed_rank, PLAYERS)

print(len(result))
for turn in result:
    print(*sorted(turn))


"""
이걸 어떻게 실전에 써먹을 수 있는 형태로 바꿀까요?
우선 L = [3, 1, 6, 10, 10, 6]
이런 형태가 있다고 가정합니다.
그러면 여기서 ε(0+)가 있다고 가정할 때
[3-ε, 1-ε, 6-ε, 10-ε, 10-2ε, 6-2ε]
이렇게 바꾸면 무조건 모든 값들을 수학적으로 다 다른 값으로 취급할 수 있습니다.
그리고 이것을 1-index 기반으로 값 압축 진행하면
[2, 1, 4, 6, 5, 3]
이렇게 됩니다.
그 뒤 플레이어가 2명일 때
3
2 6
4 5
1 3
이렇게 존재하고 이것은
3-ε 10-ε
6-ε 10-2ε
1-ε 6-2ε
해당 높이의 건물들을 다음과 같이 쏘라는 뜻입니다.

그런데 만약
4 4 2 2
이렇게 되면 어떻게 될까요?
우선 ε을 적용하여
4-ε 4-2ε 2-ε 2-2ε
이렇게 변환한 뒤 이것을 압축하여
4 3 2 1
이렇게 만들어지고 그 다음 시뮬레이션 돌려서
4 5
3 5
2 5
1 5
이런 결과를 얻은 후, N+1 -> -1로 변환합니다.(왜냐면 물리적으로 높이는 0 이상의 정수를 가지므로 -1은 허공에 쏜 것으로 취급)
참고로 -1은 허공에 쏘는 방법도 있지만 안 쏘는 방법도 있습니다.
이러면
4-ε -1
4-2ε -1
2-ε -1
2-2ε -1
이렇게 되며 여기서 플레이어가 번갈아서 총알을 쏘면
플레이어 A는 2발, 플레이어 B는 2발만 쏘면서 모든 건물을 다 부술 수 있습니다.
이 때 총을 쏘는 순서는 count = [0, 0] 이렇게 있을 때 가장 적게 쏜 플레이어부터 우선권을 가지고,
만약 이미 쐈던 총알 개수가 같은 경우 플레이어 번호가 적은 플레이어부터 우선권을 가지는 씩으로 총을 쏩니다.

예시로 count = [2, 1, 1]이고 2 5 -1 이렇게 나오면 플레이어 B와 C가 총을 1발씩 쏘고 A는 안 쏩니다.
이러면 count = [2, 2, 2]가 됩니다.
혹은 count = [2, 1, 1]일 때 2 -1 -1 이렇게 나오면 플레이어 B가 1발 쏘고 플레이어 A와 C는 안 쏩니다.
이러면 count = [2, 2, 1]가 됩니다.
이런 규칙을 볼 때 count는 항상 내림차순인 것을 알 수가 있으며 항상 max(count) - min(count) <= 1을 만족합니다.

어...? 잠만...? 이거 count를 리스트로 할 필요가 없잖아요...?
그냥 count = 0 형식으로 해서 우선 index = count % PLAYERS로 해서 해당 index의 플레이어가 1발 격발하고
그 다음 count += 1을 해주면... 오! 이거 시간, 메모리 최적화 개이득ㅋㅋㅋㅋ



나중에 제가 따로 위 시나리오 내용을 소스 코드로 구현해서 어떻게 써먹을지 생각해봐야겠어요.
"""