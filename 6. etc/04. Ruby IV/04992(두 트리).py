# 링크 : https://jungol.co.kr/problem/4992
import sys
import heapq
import random

# 에디토리얼이 없어서 상당히 오래 걸렸네요.
# 백준 링크 : https://www.acmicpc.net/problem/24027

class PeelStep:
    __slots__ = ("blue_leaf", "blue_parent", "red_leaf", "red_parent")

    def __init__(self, blue_leaf:int, blue_parent:int, red_leaf:int, red_parent:int) -> None:
        self.blue_leaf:int = blue_leaf
        self.blue_parent:int = blue_parent
        self.red_leaf:int = red_leaf
        self.red_parent:int = red_parent

class TreeData:
    __slots__ = (
        "adjacency_list",
        "degree",
        "parent_node",
        "attached_leaves",
        "internal_degree",
        "is_removed",
        "internal_node_count",
        "peel_queue",
    )

    def __init__(self, N:int) -> None:
        self.adjacency_list:list = [[] for _ in range(N + 1)]
        self.degree:list = [0] * (N + 1)
        self.parent_node:list = [0] * (N + 1)
        self.attached_leaves:list = [[] for _ in range(N + 1)]
        self.internal_degree:list = [0] * (N + 1)
        self.is_removed:list = [False] * (N + 1)
        self.internal_node_count:int = 0
        self.peel_queue:list = []

# 1. 트리 간선 입력 처리
def read_tree_input(tree:TreeData, N:int) -> None:
    for _ in range(N - 1):
        first_node:int = int(next(token_iterator))
        second_node:int = int(next(token_iterator))
        tree.adjacency_list[first_node].append(second_node)
        tree.adjacency_list[second_node].append(first_node)
        tree.degree[first_node] += 1
        tree.degree[second_node] += 1

# 2. 스타 그래프(최대 차수가 N - 1인 트리) 여부 판별
def is_star_graph(tree:TreeData, N:int) -> bool:
    for node_index in range(1, N + 1):
        if tree.degree[node_index] == N - 1:
            return True
    return False

# 3. O(1) 간선 확인을 위한 루트 트리 부모 테이블 구축(BFS)
def build_rooted_parent_table(tree:TreeData, N:int) -> None:
    breadth_first_search_queue:list = [1]
    tree.parent_node[1] = -1

    head_index:int = 0
    while head_index < len(breadth_first_search_queue):
        current_node:int = breadth_first_search_queue[head_index]
        head_index += 1
        for next_node in tree.adjacency_list[current_node]:
            if next_node != tree.parent_node[current_node]:
                tree.parent_node[next_node] = current_node
                breadth_first_search_queue.append(next_node)

# 두 정점 사이에 간선이 존재하는지 O(1)에 판별
def has_edge(tree:TreeData, first_node:int, second_node:int) -> bool:
    return tree.parent_node[first_node] == second_node or tree.parent_node[second_node] == first_node

# 4. 리프 제거(Peeling)를 위한 초기 차수 및 우선순위 큐 세팅
def initialize_peeling_state(tree:TreeData, N:int) -> None:
    for current_node in range(1, N + 1):
        if tree.degree[current_node] >= 2:
            tree.internal_node_count += 1
        for neighbor_node in tree.adjacency_list[current_node]:
            if tree.degree[neighbor_node] == 1:
                tree.attached_leaves[current_node].append(neighbor_node)
            else:
                tree.internal_degree[current_node] += 1

    for current_node in range(1, N + 1):
        if tree.degree[current_node] >= 2 and tree.internal_degree[current_node] == 1:
            heapq.heappush(tree.peel_queue, (tree.degree[current_node], current_node))

# 5. 트리에서 조건을 만족하는 리프 하나를 깎아내고 (리프, 부모) 쌍을 반환
def peel_single_leaf(tree:TreeData) -> tuple:
    selected_parent:int = -1

    while tree.peel_queue:
        top_element:tuple = heapq.heappop(tree.peel_queue)
        recorded_degree:int = top_element[0]
        candidate_node:int = top_element[1]

        if tree.is_removed[candidate_node]:
            continue
        if tree.degree[candidate_node] != recorded_degree:
            continue
        if tree.degree[candidate_node] < 2 or tree.internal_degree[candidate_node] != 1:
            continue

        selected_parent = candidate_node
        break

    selected_leaf:int = tree.attached_leaves[selected_parent].pop()

    tree.is_removed[selected_leaf] = True
    tree.degree[selected_leaf] = 0
    tree.degree[selected_parent] -= 1

    if tree.degree[selected_parent] >= 2:
        heapq.heappush(tree.peel_queue, (tree.degree[selected_parent], selected_parent))
    else:
        # 부모 정점의 차수가 1이 되어 새로운 리프로 전환되는 경우
        tree.internal_node_count -= 1
        next_parent:int = -1

        for next_node in tree.adjacency_list[selected_parent]:
            if not tree.is_removed[next_node]:
                next_parent = next_node
                break

        tree.attached_leaves[next_parent].append(selected_parent)
        tree.internal_degree[next_parent] -= 1

        if tree.degree[next_parent] >= 2 and tree.internal_degree[next_parent] == 1:
            heapq.heappush(tree.peel_queue, (tree.degree[next_parent], next_parent))

    return (selected_leaf, selected_parent)

# 매칭 배열에 (파란 정점 -> 빨간 정점) 대응을 기록하는 보조 함수
def assign_node_pair(
    blue_node:int,
    red_node:int,
    blue_to_red_mapping:list,
    is_blue_matched:list,
    is_red_matched:list
) -> None:
    blue_to_red_mapping[blue_node] = red_node
    is_blue_matched[blue_node] = True
    is_red_matched[red_node] = True

# 6. 기저 상태: 한쪽 트리가 이중 스타(내부 정점 2개)가 되었을 때 초기 매칭 구성
def match_double_star_base_case(
    red_tree:TreeData,
    blue_tree:TreeData,
    active_red_nodes:list,
    active_blue_nodes:list,
    blue_to_red_mapping:list,
    N:int
) -> None:
    is_red_matched:list = [False] * (N + 1)
    is_blue_matched:list = [False] * (N + 1)

    if red_tree.internal_node_count == 2:
        red_centers:list = []
        for current_node in active_red_nodes:
            if red_tree.degree[current_node] >= 2:
                red_centers.append(current_node)

        first_red_center:int = red_centers[0]
        second_red_center:int = red_centers[1]
        first_red_leaf:int = red_tree.attached_leaves[first_red_center][0]
        second_red_leaf:int = red_tree.attached_leaves[second_red_center][0]

        blue_parents:list = []
        for current_node in active_blue_nodes:
            if blue_tree.degree[current_node] >= 2 and blue_tree.attached_leaves[current_node]:
                blue_parents.append(current_node)
                if len(blue_parents) == 2:
                    break

        first_blue_parent:int = blue_parents[0]
        second_blue_parent:int = blue_parents[1]
        first_blue_leaf:int = blue_tree.attached_leaves[first_blue_parent][0]
        second_blue_leaf:int = blue_tree.attached_leaves[second_blue_parent][0]

        assign_node_pair(first_blue_leaf, first_red_center, blue_to_red_mapping, is_blue_matched, is_red_matched)
        assign_node_pair(second_blue_leaf, second_red_center, blue_to_red_mapping, is_blue_matched, is_red_matched)
        assign_node_pair(first_blue_parent, second_red_leaf, blue_to_red_mapping, is_blue_matched, is_red_matched)
        assign_node_pair(second_blue_parent, first_red_leaf, blue_to_red_mapping, is_blue_matched, is_red_matched)
    else:
        blue_centers:list = []
        for current_node in active_blue_nodes:
            if blue_tree.degree[current_node] >= 2:
                blue_centers.append(current_node)

        first_blue_center:int = blue_centers[0]
        second_blue_center:int = blue_centers[1]
        first_blue_leaf:int = blue_tree.attached_leaves[first_blue_center][0]
        second_blue_leaf:int = blue_tree.attached_leaves[second_blue_center][0]

        red_parents:list = []
        for current_node in active_red_nodes:
            if red_tree.degree[current_node] >= 2 and red_tree.attached_leaves[current_node]:
                red_parents.append(current_node)
                if len(red_parents) == 2:
                    break

        first_red_parent:int = red_parents[0]
        second_red_parent:int = red_parents[1]
        first_red_leaf:int = red_tree.attached_leaves[first_red_parent][0]
        second_red_leaf:int = red_tree.attached_leaves[second_red_parent][0]

        assign_node_pair(first_blue_center, first_red_leaf, blue_to_red_mapping, is_blue_matched, is_red_matched)
        assign_node_pair(second_blue_center, second_red_leaf, blue_to_red_mapping, is_blue_matched, is_red_matched)
        assign_node_pair(second_blue_leaf, first_red_parent, blue_to_red_mapping, is_blue_matched, is_red_matched)
        assign_node_pair(first_blue_leaf, second_red_parent, blue_to_red_mapping, is_blue_matched, is_red_matched)

    # 남은 기저 정점들을 순서대로 1:1 매칭
    red_position:int = 0
    for blue_node in active_blue_nodes:
        if is_blue_matched[blue_node]:
            continue
        while is_red_matched[active_red_nodes[red_position]]:
            red_position += 1
        assign_node_pair(blue_node, active_red_nodes[red_position], blue_to_red_mapping, is_blue_matched, is_red_matched)

# 7. 제거했던 리프들을 역순으로 복원하며 간선 충돌 시 스왑으로 해결
def unwind_and_repair_matching(
    red_tree:TreeData,
    blue_tree:TreeData,
    peel_stack:list,
    active_blue_nodes:list,
    blue_to_red_mapping:list
) -> None:
    random_generator:random.Random = random.Random(1337)
    scan_index:int = 0

    while peel_stack:
        current_step:PeelStep = peel_stack.pop()

        blue_leaf:int = current_step.blue_leaf
        blue_parent:int = current_step.blue_parent
        red_leaf:int = current_step.red_leaf
        red_parent:int = current_step.red_parent

        if blue_to_red_mapping[blue_parent] != red_parent:
            blue_to_red_mapping[blue_leaf] = red_leaf
        else:
            swap_target_blue:int = -1
            active_size:int = len(active_blue_nodes)

            # 무작위 샘플링으로 충돌 없는 스왑 대상 탐색
            for _ in range(24):
                candidate_node:int = active_blue_nodes[random_generator.randrange(active_size)]
                if (
                    candidate_node != blue_parent
                    and not has_edge(blue_tree, candidate_node, blue_parent)
                    and not has_edge(red_tree, blue_to_red_mapping[candidate_node], red_parent)
                ):
                    swap_target_blue = candidate_node
                    break

            # 무작위 탐색에서 찾지 못한 경우 순차 스캔으로 확정 탐색
            if swap_target_blue == -1:
                for offset in range(active_size):
                    candidate_node = active_blue_nodes[(scan_index + offset) % active_size]
                    if (
                        candidate_node != blue_parent
                        and not has_edge(blue_tree, candidate_node, blue_parent)
                        and not has_edge(red_tree, blue_to_red_mapping[candidate_node], red_parent)
                    ):
                        swap_target_blue = candidate_node
                        scan_index = (scan_index + offset + 1) % active_size
                        break

            blue_to_red_mapping[blue_leaf] = blue_to_red_mapping[swap_target_blue]
            blue_to_red_mapping[swap_target_blue] = red_leaf

        active_blue_nodes.append(blue_leaf)

input_tokens:list = sys.stdin.read().split()
token_iterator = iter(input_tokens)

N:int = int(next(token_iterator))

red_tree:TreeData = TreeData(N)
blue_tree:TreeData = TreeData(N)

read_tree_input(red_tree, N)
read_tree_input(blue_tree, N)

# 스타 그래프가 하나라도 있으면 매칭 불가능
if is_star_graph(red_tree, N) or is_star_graph(blue_tree, N):
    sys.stdout.write("-1\n")
else:
    build_rooted_parent_table(red_tree, N)
    build_rooted_parent_table(blue_tree, N)

    initialize_peeling_state(red_tree, N)
    initialize_peeling_state(blue_tree, N)

    peel_stack:list = []

    # 두 트리 중 하나가 이중 스타가 될 때까지 양쪽에서 리프를 하나씩 제거
    while red_tree.internal_node_count >= 3 and blue_tree.internal_node_count >= 3:
        red_peeled:tuple = peel_single_leaf(red_tree)
        blue_peeled:tuple = peel_single_leaf(blue_tree)

        current_step:PeelStep = PeelStep(
            blue_peeled[0],
            blue_peeled[1],
            red_peeled[0],
            red_peeled[1]
        )
        peel_stack.append(current_step)

    active_red_nodes:list = []
    active_blue_nodes:list = []

    for node_index in range(1, N + 1):
        if not red_tree.is_removed[node_index]:
            active_red_nodes.append(node_index)
        if not blue_tree.is_removed[node_index]:
            active_blue_nodes.append(node_index)

    blue_to_red_mapping:list = [0] * (N + 1)

    # 기저 조건 매칭 후 역순으로 리프 복원
    match_double_star_base_case(
        red_tree,
        blue_tree,
        active_red_nodes,
        active_blue_nodes,
        blue_to_red_mapping,
        N
    )
    unwind_and_repair_matching(
        red_tree,
        blue_tree,
        peel_stack,
        active_blue_nodes,
        blue_to_red_mapping
    )

    # 최종 결과 출력
    sys.stdout.write(" ".join(str(blue_to_red_mapping[node_index]) for node_index in range(1, N + 1)) + "\n")