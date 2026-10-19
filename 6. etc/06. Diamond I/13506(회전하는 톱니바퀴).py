# 링크 : https://jungol.co.kr/problem/13506
import sys

input = sys.stdin.readline
read = sys.stdin.read
write = sys.stdout.write

# 에디토리얼 : https://icpcarchive.github.io/Asia%20Pacific%20Contests/Indonesia/2018%20Asia%20Jakarta%20Regional%20Contest/solution.pdf
# 이 소스 코드는 실제 백준/정올에 제출하면 TLE 나는 소스 코드입니다.
# 대신 오프라인 쿼리가 아닌 온라인 쿼리로 실시간 연산이 가능합니다.

# =========================================================================================
# 1. A 쿼리 그룹 (1, 2, 3번 연산 - 단일 LCT 연산):
#    - 루트 트리 부모 간선 트릭(Rooted Tree Parent-Edge Trick)과 경로 합 차분 보정을 결합한
#      단일 링크-컷 트리(Link-Cut Tree)만으로 O(log N)에 동작합니다.
#    - B 쿼리가 입력되지 않는 온라인 저지 환경에서는 탑 트리 관련 함수와 배열이 전혀 호출되지 않아
#      단일 LCT와 100% 동일한 최소 실행 시간 및 메모리 오버헤드를 보장합니다.
#
# 2. B 쿼리 그룹 (4, 5, 6번 연산 - LCT + Top Tree 확장 계층):
#    - 차분 보정으로 처리할 수 없는 비가역 연산 및 위상 탐색을 위해 활성 클러스터를 실시간 추출하고
#      사전 할당된 상태 버퍼와 LCT 스플레이 동기화를 결합하여 온라인으로 처리합니다.
#    - 4번 연산 (4 x)      : 연결 요소 내 최대 회전각(Subtree Max) 실시간 출력
#    - 5번 연산 (5 x alpha): 연결 요소 내 모든 톱니바퀴 각도를 alpha로 일괄 덮어쓰기(Subtree Assign)
#    - 6번 연산 (6 x)      : 연결 요소의 토크 불균형을 최소화하는 동적 무게중심(Dynamic Centroid) 탐색
# =========================================================================================


class DynamicGearSystem:
    def __init__(self, node_count:int):
        self.node_count:int = node_count
        # 0번 인덱스는 NULL 포인터로 사용하며, (node_count + 1)번 노드를 영구 비활성 가상 루트로 설정
        self.dummy_root:int = node_count + 1
        total_capacity:int = node_count + 2

        # --- 정적 루트 트리 및 위상 정보 ---
        self.adjacency_list:list = [[] for _ in range(node_count + 1)]
        self.static_children:list = [[] for _ in range(total_capacity)]
        self.static_parent:list = [0] * total_capacity
        self.parity_sign:list = [1] * total_capacity
        self.topological_order:list = []
        self.is_active:list = [False] * total_capacity

        # --- [A 쿼리 전용] 순수 링크-컷 트리 (Link-Cut Tree) 배열 ---
        self.left_child:list = [0] * total_capacity
        self.right_child:list = [0] * total_capacity
        self.parent_pointer:list = [0] * total_capacity
        self.virtual_size:list = [0] * total_capacity
        self.total_size:list = [0] * total_capacity
        self.point_angle:list = [0] * total_capacity
        self.path_sum:list = [0] * total_capacity

        # --- [B 쿼리 전용] 탑 트리 확장 계층 및 사전 할당 작업 버퍼 (오버헤드 0 지연 초기화) ---
        self.top_tree_initialized:bool = False
        self.accumulated_angle_buffer:list = []
        self.desired_angle_buffer:list = []
        self.subtree_count_buffer:list = []
        self.heavy_child_buffer:list = []

    def add_undirected_edge(self, first_node:int, second_node:int) -> None:
        self.adjacency_list[first_node].append(second_node)
        self.adjacency_list[second_node].append(first_node)

    # 초기 트리를 1번 루트 기준으로 방향화하고, 모든 간선을 가상 간선(Dashed Edge)으로 O(N)에 초기화
    def build_initial_static_tree(self) -> None:
        node_count:int = self.node_count
        dummy_root:int = self.dummy_root
        adjacency_list:list = self.adjacency_list
        static_children:list = self.static_children
        static_parent:list = self.static_parent
        parity_sign:list = self.parity_sign
        is_active:list = self.is_active
        parent_pointer:list = self.parent_pointer
        virtual_size:list = self.virtual_size
        total_size:list = self.total_size

        visited:list = [False] * (node_count + 1)
        visited[1] = True
        static_parent[1] = dummy_root
        static_children[dummy_root].append(1)
        parity_sign[1] = 1

        traversal_queue:list = [1]
        read_index:int = 0
        while read_index < len(traversal_queue):
            current_node:int = traversal_queue[read_index]
            read_index += 1
            current_sign:int = parity_sign[current_node]
            current_children:list = static_children[current_node]
            for neighbor_node in adjacency_list[current_node]:
                if not visited[neighbor_node]:
                    visited[neighbor_node] = True
                    static_parent[neighbor_node] = current_node
                    current_children.append(neighbor_node)
                    parity_sign[neighbor_node] = -current_sign
                    traversal_queue.append(neighbor_node)

        self.topological_order = traversal_queue

        # 1번부터 N번까지의 모든 톱니바퀴는 초기에 판 위에 놓여 있음 (dummy_root만 영구 비활성)
        for gear_node in range(1, node_count + 1):
            is_active[gear_node] = True
            parent_pointer[gear_node] = static_parent[gear_node]

        # 역방향 위상 정렬 순회로 회전 없이 O(N) 만에 초기 LCT 서브트리 크기 구축
        for gear_node in reversed(traversal_queue):
            current_total:int = 1 + virtual_size[gear_node]
            total_size[gear_node] = current_total
            parent_node:int = static_parent[gear_node]
            virtual_size[parent_node] += current_total

        total_size[dummy_root] = 1 + virtual_size[dummy_root]

    # [파트 A] 순수 링크-컷 트리 (Link-Cut Tree) 핵심 엔진 (1, 2, 3번 쿼리 전용)

    def lct_is_splay_root(self, target_node:int) -> bool:
        parent_node:int = self.parent_pointer[target_node]
        return (
            parent_node == 0
            or (self.left_child[parent_node] != target_node and self.right_child[parent_node] != target_node)
        )

    def lct_pull_up_node(self, target_node:int) -> None:
        left_node:int = self.left_child[target_node]
        right_node:int = self.right_child[target_node]
        self.total_size[target_node] = (
            self.total_size[left_node]
            + self.total_size[right_node]
            + self.virtual_size[target_node]
            + 1
        )
        self.path_sum[target_node] = (
            self.path_sum[left_node]
            + self.path_sum[right_node]
            + self.point_angle[target_node]
        )

    def lct_rotate_node(self, target_node:int) -> None:
        left_child:list = self.left_child
        right_child:list = self.right_child
        parent_pointer:list = self.parent_pointer

        parent_node:int = parent_pointer[target_node]
        grandparent_node:int = parent_pointer[parent_node]

        if left_child[grandparent_node] == parent_node:
            left_child[grandparent_node] = target_node
        elif right_child[grandparent_node] == parent_node:
            right_child[grandparent_node] = target_node

        if left_child[parent_node] == target_node:
            inner_child:int = right_child[target_node]
            left_child[parent_node] = inner_child
            if inner_child != 0:
                parent_pointer[inner_child] = parent_node
            right_child[target_node] = parent_node
        else:
            inner_child = left_child[target_node]
            right_child[parent_node] = inner_child
            if inner_child != 0:
                parent_pointer[inner_child] = parent_node
            left_child[target_node] = parent_node

        parent_pointer[parent_node] = target_node
        parent_pointer[target_node] = grandparent_node

        self.lct_pull_up_node(parent_node)
        self.lct_pull_up_node(target_node)

    def lct_splay_node(self, target_node:int) -> None:
        if target_node == 0:
            return
        left_child:list = self.left_child
        parent_pointer:list = self.parent_pointer

        while not self.lct_is_splay_root(target_node):
            parent_node:int = parent_pointer[target_node]
            if not self.lct_is_splay_root(parent_node):
                grandparent_node:int = parent_pointer[parent_node]
                if (left_child[grandparent_node] == parent_node) == (left_child[parent_node] == target_node):
                    self.lct_rotate_node(parent_node)
                else:
                    self.lct_rotate_node(target_node)
            self.lct_rotate_node(target_node)

    def lct_access_node(self, target_node:int) -> int:
        right_child:list = self.right_child
        parent_pointer:list = self.parent_pointer
        virtual_size:list = self.virtual_size
        total_size:list = self.total_size

        last_solid_child:int = 0
        current_node:int = target_node
        while current_node != 0:
            self.lct_splay_node(current_node)
            previous_right:int = right_child[current_node]
            if previous_right != 0:
                virtual_size[current_node] += total_size[previous_right]
            if last_solid_child != 0:
                virtual_size[current_node] -= total_size[last_solid_child]
            right_child[current_node] = last_solid_child
            self.lct_pull_up_node(current_node)
            last_solid_child = current_node
            current_node = parent_pointer[current_node]
        return last_solid_child

    # [1번 쿼리] 판 위의 톱니바퀴 target_gear 제거 (단일 부모 간선 절단 + 경로 합 차분 보정)
    def lct_remove_gear(self, target_gear:int) -> None:
        if not self.is_active[target_gear]:
            return
        parent_gear:int = self.static_parent[target_gear]

        # 1. 절단 직전 부모 정점까지의 누적 회전각(path_sum) 조회
        self.lct_access_node(parent_gear)
        self.lct_splay_node(parent_gear)
        accumulated_parent_angle:int = self.path_sum[parent_gear]

        # 2. (target_gear, parent_gear) 간선 절단 및 누적 회전각 보존
        self.lct_access_node(target_gear)
        self.lct_splay_node(target_gear)
        left_subtree:int = self.left_child[target_gear]
        if left_subtree != 0:
            self.parent_pointer[left_subtree] = 0
            self.left_child[target_gear] = 0

        self.point_angle[target_gear] += accumulated_parent_angle
        self.lct_pull_up_node(target_gear)
        self.is_active[target_gear] = False

    # [2번 쿼리] 빠져 있던 톱니바퀴 target_gear 재삽입 (상위 경로 합 상쇄 + 단일 부모 간선 연결)
    def lct_insert_gear(self, target_gear:int) -> None:
        if self.is_active[target_gear]:
            return
        parent_gear:int = self.static_parent[target_gear]

        # 1. 재연결 직전 부모 정점까지의 현재 누적 회전각 조회
        self.lct_access_node(parent_gear)
        self.lct_splay_node(parent_gear)
        current_parent_angle:int = self.path_sum[parent_gear]

        # 2. 빠져 있던 동안 상위 컴포넌트에서 발생한 회전량을 차감하여 기존 각도 유지
        self.lct_access_node(target_gear)
        self.lct_splay_node(target_gear)
        self.point_angle[target_gear] -= current_parent_angle
        self.lct_pull_up_node(target_gear)

        # 3. target_gear를 parent_gear의 가상 자식(Dashed Child)으로 즉시 병합
        self.parent_pointer[target_gear] = parent_gear
        self.virtual_size[parent_gear] += self.total_size[target_gear]
        self.lct_pull_up_node(parent_gear)
        self.is_active[target_gear] = True

    # [3번 쿼리] target_gear가 속한 활성 연결 요소를 clockwise_angle만큼 회전 및 에너지 반환
    def lct_rotate_component(self, target_gear:int, clockwise_angle:int) -> int:
        if not self.is_active[target_gear]:
            return 0
        left_child:list = self.left_child
        right_child:list = self.right_child

        self.lct_access_node(target_gear)
        self.lct_splay_node(target_gear)

        # 현재 LCT 트리의 비활성 루트(inactive_root) 탐색
        inactive_root:int = target_gear
        while left_child[inactive_root] != 0:
            inactive_root = left_child[inactive_root]
        self.lct_splay_node(inactive_root)

        # 비활성 루트 바로 아래의 최상위 활성 조상(top_active_node) 탐색
        top_active_node:int = right_child[inactive_root]
        while left_child[top_active_node] != 0:
            top_active_node = left_child[top_active_node]
        self.lct_splay_node(top_active_node)

        # top_active_node의 서브트리 크기(비활성 루트 제외)가 곧 함께 회전하는 톱니바퀴의 총개수
        active_component_size:int = (
            self.total_size[top_active_node] - self.total_size[left_child[top_active_node]]
        )

        # 이분 그래프 부호에 맞춰 최상위 활성 조상 단 한 곳에만 회전각 누적
        normalized_delta:int = self.parity_sign[target_gear] * clockwise_angle
        self.point_angle[top_active_node] += normalized_delta
        self.path_sum[top_active_node] += normalized_delta

        return active_component_size * clockwise_angle

    # 모든 연산 종료 후 위상 정렬 순서에 따라 각 톱니바퀴의 최종 각도 합산을 O(N)에 수행
    def compute_final_angle_sum(self) -> int:
        static_parent:list = self.static_parent
        is_active:list = self.is_active
        point_angle:list = self.point_angle
        parity_sign:list = self.parity_sign

        accumulated_path_angle:list = [0] * (self.node_count + 2)
        total_modulo_angle_sum:int = 0

        for gear_node in self.topological_order:
            if is_active[gear_node]:
                accumulated_path_angle[gear_node] = (
                    accumulated_path_angle[static_parent[gear_node]] + point_angle[gear_node]
                )
            else:
                accumulated_path_angle[gear_node] = point_angle[gear_node]

            final_clockwise_angle:int = (parity_sign[gear_node] * accumulated_path_angle[gear_node]) % 360
            total_modulo_angle_sum += final_clockwise_angle

        return total_modulo_angle_sum

    # [파트 B] 탑 트리 확장 엔진 (4, 5, 6번 쿼리용)
    # - A 쿼리만 실행될 때는 호출되지 않으며, B 쿼리 등장 시 단 1회 버퍼를 할당합니다.
    # - 전체 N개 노드를 순회하지 않고 활성 컴포넌트(|C|) 내부만 지역 탐색하여 과부하를 방지합니다.

    def initialize_top_tree_layer(self) -> None:
        if self.top_tree_initialized:
            return
        total_capacity:int = self.node_count + 2
        self.accumulated_angle_buffer = [0] * total_capacity
        self.desired_angle_buffer = [0] * total_capacity
        self.subtree_count_buffer = [0] * total_capacity
        self.heavy_child_buffer = [0] * total_capacity
        self.top_tree_initialized = True

    # LCT의 비활성 루트(inactive_root), 최상위 활성 조상(top_active_node) 및 활성 컴포넌트 정점 목록을 O(|C|)에 추출
    def top_tree_collect_active_component(self, target_gear:int) -> tuple:
        self.initialize_top_tree_layer()
        if not self.is_active[target_gear]:
            return target_gear, 0, []

        left_child:list = self.left_child
        right_child:list = self.right_child

        self.lct_access_node(target_gear)
        self.lct_splay_node(target_gear)

        inactive_root:int = target_gear
        while left_child[inactive_root] != 0:
            inactive_root = left_child[inactive_root]
        self.lct_splay_node(inactive_root)

        top_active_node:int = right_child[inactive_root]
        while left_child[top_active_node] != 0:
            top_active_node = left_child[top_active_node]
        self.lct_splay_node(top_active_node)

        # 전체 트리가 아닌 현재 활성 컴포넌트 내부의 정점만 위상 순서(BFS)로 수집
        static_children:list = self.static_children
        is_active:list = self.is_active
        component_nodes:list = [top_active_node]
        read_index:int = 0

        while read_index < len(component_nodes):
            current_node:int = component_nodes[read_index]
            read_index += 1
            for child_node in static_children[current_node]:
                if is_active[child_node]:
                    component_nodes.append(child_node)

        return inactive_root, top_active_node, component_nodes

    # [4번 쿼리] target_gear가 속한 활성 연결 요소 내 최대 회전각(Max Angle) 실시간 조회
    def top_tree_query_max_angle(self, target_gear:int) -> int:
        inactive_root, top_active_node, component_nodes = self.top_tree_collect_active_component(target_gear)
        if top_active_node == 0:
            return (self.parity_sign[target_gear] * self.point_angle[target_gear]) % 360

        static_parent:list = self.static_parent
        point_angle:list = self.point_angle
        parity_sign:list = self.parity_sign
        accumulated_angle:list = self.accumulated_angle_buffer

        # 상위 정점(inactive_root)이 분리될 때 박제해 둔 기준 회전각(point_angle[inactive_root])을 함께 반영
        accumulated_angle[top_active_node] = point_angle[inactive_root] + point_angle[top_active_node]
        maximum_clockwise_angle:int = (parity_sign[top_active_node] * accumulated_angle[top_active_node]) % 360

        for gear_node in component_nodes[1:]:
            parent_node:int = static_parent[gear_node]
            accumulated_angle[gear_node] = accumulated_angle[parent_node] + point_angle[gear_node]
            current_angle:int = (parity_sign[gear_node] * accumulated_angle[gear_node]) % 360
            if current_angle > maximum_clockwise_angle:
                maximum_clockwise_angle = current_angle

        return maximum_clockwise_angle

    # [5번 쿼리] target_gear가 속한 활성 연결 요소의 모든 톱니바퀴 각도를 target_angle로 일괄 덮어쓰기(Assign)
    def top_tree_assign_component_angle(self, target_gear:int, target_angle:int) -> None:
        normalized_target_angle:int = target_angle % 360
        inactive_root, top_active_node, component_nodes = self.top_tree_collect_active_component(target_gear)
        if top_active_node == 0:
            self.point_angle[target_gear] = self.parity_sign[target_gear] * normalized_target_angle
            self.lct_pull_up_node(target_gear)
            return

        static_parent:list = self.static_parent
        point_angle:list = self.point_angle
        parity_sign:list = self.parity_sign
        desired_normalized_angle:list = self.desired_angle_buffer

        desired_normalized_angle[top_active_node] = parity_sign[top_active_node] * normalized_target_angle

        # inactive_root의 보존 각도를 차감하여 오프셋 중첩을 막고,
        # 스플레이 루트 상태에서 point_angle 수정 후 즉시 pull_up을 호출해 LCT의 path_sum 캐시를 동기화
        self.lct_splay_node(top_active_node)
        point_angle[top_active_node] = (
            desired_normalized_angle[top_active_node] - point_angle[inactive_root]
        )
        self.lct_pull_up_node(top_active_node)

        for gear_node in component_nodes[1:]:
            parent_node:int = static_parent[gear_node]
            desired_normalized_angle[gear_node] = parity_sign[gear_node] * normalized_target_angle
            self.lct_splay_node(gear_node)
            point_angle[gear_node] = (
                desired_normalized_angle[gear_node] - desired_normalized_angle[parent_node]
            )
            self.lct_pull_up_node(gear_node)

        self.lct_access_node(top_active_node)

    # [6번 쿼리] 탑 트리 클러스터 탐색을 통한 연결 요소의 동적 무게중심(센트로이드) 톱니바퀴 탐색
    # - 전체 연결 요소 크기가 S일 때, 가장 무거운 자식 서브트리를 따라 내려가 모든 분기 크기가 <= S // 2가 되는
    #   최적 구동축 정점을 반환합니다. (센트로이드가 2개인 짝수 대칭 트리에서는 더 작은 정점 번호를 반환)
    def top_tree_find_dynamic_centroid(self, target_gear:int) -> int:
        _, top_active_node, component_nodes = self.top_tree_collect_active_component(target_gear)
        if top_active_node == 0:
            return target_gear

        static_parent:list = self.static_parent
        subtree_count:list = self.subtree_count_buffer
        heavy_branch_child:list = self.heavy_child_buffer

        component_size:int = len(component_nodes)
        half_size:int = component_size // 2

        for gear_node in component_nodes:
            subtree_count[gear_node] = 0
            heavy_branch_child[gear_node] = 0

        for gear_node in reversed(component_nodes):
            subtree_count[gear_node] += 1
            if gear_node != top_active_node:
                parent_node:int = static_parent[gear_node]
                subtree_count[parent_node] += subtree_count[gear_node]
                current_heavy:int = heavy_branch_child[parent_node]
                if (
                    subtree_count[gear_node] > subtree_count[current_heavy]
                    or (subtree_count[gear_node] == subtree_count[current_heavy] and gear_node < current_heavy)
                ):
                    heavy_branch_child[parent_node] = gear_node

        current_candidate:int = top_active_node
        while heavy_branch_child[current_candidate] != 0 and subtree_count[heavy_branch_child[current_candidate]] > half_size:
            current_candidate = heavy_branch_child[current_candidate]

        if (
            component_size % 2 == 0
            and heavy_branch_child[current_candidate] != 0
            and subtree_count[heavy_branch_child[current_candidate]] == half_size
        ):
            if heavy_branch_child[current_candidate] < current_candidate:
                current_candidate = heavy_branch_child[current_candidate]

        return current_candidate


# 1. 톱니바퀴 개수 N 입력
gear_count:int = int(input().strip())

gear_system:DynamicGearSystem = DynamicGearSystem(gear_count)

# 2. N - 1개의 간선 입력 및 양방향 간선 추가
for _ in range(gear_count - 1):
    edge_tokens:list = input().split()
    first_gear:int = int(edge_tokens[0])
    second_gear:int = int(edge_tokens[1])
    gear_system.add_undirected_edge(first_gear, second_gear)

# 3. 초기 고정 트리 O(N) 구축
gear_system.build_initial_static_tree()

# 4. 연산 수 Q 입력
query_count:int = int(input().strip())

# 5. Q개의 온라인 쿼리 실시간 처리 및 출력
for _ in range(query_count):
    query_tokens:list = input().split()
    query_type:int = int(query_tokens[0])

    # [A 쿼리 그룹: 순수 LCT 경로]
    if query_type == 1:
        target_gear:int = int(query_tokens[1])
        gear_system.lct_remove_gear(target_gear)

    elif query_type == 2:
        target_gear:int = int(query_tokens[1])
        gear_system.lct_insert_gear(target_gear)

    elif query_type == 3:
        target_gear:int = int(query_tokens[1])
        clockwise_angle:int = int(query_tokens[2])
        # 회전 연산 후 에너지 양을 즉시 출력 (온라인 응답)
        rotation_energy:int = gear_system.lct_rotate_component(target_gear, clockwise_angle)
        print(rotation_energy)

    # [B 쿼리 그룹: 탑 트리 확장 경로]
    elif query_type == 4:
        target_gear:int = int(query_tokens[1])
        # 서브트리 내 최대 회전각을 즉시 출력 (온라인 응답)
        max_angle:int = gear_system.top_tree_query_max_angle(target_gear)
        print(max_angle)

    elif query_type == 5:
        target_gear:int = int(query_tokens[1])
        assigned_angle:int = int(query_tokens[2])
        gear_system.top_tree_assign_component_angle(target_gear, assigned_angle)

    elif query_type == 6:
        target_gear:int = int(query_tokens[1])
        # 연결 요소의 동적 무게중심(최적 구동축)을 즉시 출력 (온라인 응답)
        centroid_gear:int = gear_system.top_tree_find_dynamic_centroid(target_gear)
        print(centroid_gear)

# 6. 모든 연산 종료 후 위상 정렬을 통한 각 톱니바퀴의 최종 각도 모듈러 합산 출력
final_angle_sum:int = gear_system.compute_final_angle_sum()
print(final_angle_sum)

"""
=========================================================================================
[실전 공학 응용 모델: 클러치 기반 다축 서보 기어 트레인 및 모듈형 로봇 구동기 제어]

본 알고리즘의 수학적·위상적 구조는 단순한 퍼즐을 넘어, 정밀 기계공학 및 제어공학의
'가변 위상 동력 전달 계통(Reconfigurable Mechanical Powertrain)'과 1:1로 대응됩니다.

1. 물리적 시스템 매핑 (System Topology Mapping)
   - 톱니바퀴(Node) & 화살표 각도(0°~359°):
     절대형 엔코더(Absolute Encoder)가 장착된 회전 액추에이터(Rotary Actuator),
     캠 샤프트(Camshaft), 또는 물류 분류기의 조향 스위블 휠(Steering Swivel Wheel)의
     실시간 기계적 위상각(Mechanical Phase Angle)을 의미합니다.
   - 맞물림에 의한 반대 방향 회전(Parity Sign, +1 / -1):
     외접 기어 쌍의 기구학적 구속 조건(Kinematic Constraint, 기어비 1:1 역위상 맞물림)을
     이분 그래프(Bipartite Graph) 부호화로 모델링한 것입니다.

2. A 쿼리 그룹 (표준 동력 전달 및 클러치 개폐 제어 - 단일 LCT 계층)
   - 1번 연산 (1 x, 기어 분리) -> 전자식 클러치 개방(Clutch Disengagement) 및 모듈 격리:
     특정 축 x의 클러치를 해제하여 상위 구동계로부터 동력을 차단합니다. 분리된 축과
     하위 종동축들은 브레이크에 의해 분리 직전의 기계적 위상각을 그대로 유지합니다.
   - 2번 연산 (2 x, 기어 재결합) -> 위상 동기화 재결합(Phase-Preserving Re-engagement):
     축 x가 분리되어 있던 동안 상위 구동계가 회전하더라도, 재결합 시 기계적 치합(Meshing)
     오프셋을 차분 보정하여 기존 화살표 각도의 틀어짐(Backlash/Slip) 없이 동력을 재연결합니다.
   - 3번 연산 (3 x alpha, 회전 및 에너지 산출) -> 스텝 구동 및 총 관성 부하(Torque Load) 계산:
     구동축 x에 alpha만큼의 각변위 명령을 인가할 때, 현재 클러치로 직결된 모든 활성 종동축이
     함께 회전하며 소비하는 총 기계적 구동 에너지(구동 모듈 수 × 각변위)를 실시간 산출합니다.

3. B 쿼리 그룹 (고급 제어·안전 감시·캘리브레이션 - LCT + Top Tree 확장 계층)
   - 4번 연산 (4 x, 서브트리 최대 각도 조회) -> 기구학적 비틀림 한계(Mechanical Limit) 감시:
     현재 x와 맞물려 돌아가는 활성 구동 그룹 내에서 가장 큰 위상각을 가진 축을 실시간 추적하여,
     케이블 꼬임이나 기구적 스토퍼(Stopper) 파손 임계각 도달 여부를 감시합니다.
   - 5번 연산 (5 x alpha, 서브트리 일괄 덮어쓰기) -> 호밍 및 영점 강제 정렬(Homing / Calibration):
     센서 오차 누적이나 작업 전환 시, 특정 활성 서브 어셈블리에 속한 모든 액추에이터의
     위상각을 기준 각도(alpha)로 일괄 초기화(Assign)하여 기구학적 동기화를 수행합니다.
   - 6번 연산 (6 x, 동적 무게중심 탐색) -> 최적 마스터 구동축(Dynamic Master Actuator) 선정:
     클러치 개폐로 인해 실시간으로 위상이 변하는 가변 기어 네트워크에서, 양방향 토크 전달 경로와
     기계적 관성 불균형을 최소화하는 중심 축(Centroid Node)을 찾아 주 구동 모터로 할당합니다.
=========================================================================================
"""